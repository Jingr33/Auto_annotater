import os

from backend.enums.image_extensions import SUPPORTED_IMAGE_EXTENSIONS
from backend.enums.model_type import ModelType


class DatasetValidator:
    def validate(self, source_path: str, model_type: ModelType | None) -> list[str]:
        if not os.path.isdir(source_path):
            raise FileNotFoundError(f'Source path does not exist: {source_path}')

        images_dir = os.path.join(source_path, 'images')
        if not os.path.isdir(images_dir):
            raise FileNotFoundError(f'Required images/ folder not found in dataset: {source_path}')

        image_files = [
            filename
            for filename in os.listdir(images_dir)
            if os.path.isfile(os.path.join(images_dir, filename))
            and os.path.splitext(filename)[1].lower() in SUPPORTED_IMAGE_EXTENSIONS
        ]
        if not image_files:
            raise FileNotFoundError(
                f'No image files found in {images_dir}. Supported formats: {", ".join(sorted(SUPPORTED_IMAGE_EXTENSIONS))}'
            )

        if model_type == ModelType.MEDSAM2:
            labels_dir = os.path.join(source_path, 'labels')
            if not os.path.isdir(labels_dir):
                raise FileNotFoundError('MEDSAM2 dataset requires a labels/ folder with YOLO bounding boxes')
            for image_file in image_files:
                label_file = os.path.join(
                    labels_dir,
                    f'{os.path.splitext(image_file)[0]}.txt',
                )
                if os.path.isfile(label_file):
                    self._validate_label(labels_dir, image_file)

        return sorted(image_files)

    def _validate_label(self, labels_dir: str, image_file: str) -> None:
        label_file = os.path.join(labels_dir, f'{os.path.splitext(image_file)[0]}.txt')
        if not os.path.isfile(label_file):
            raise FileNotFoundError(f'MEDSAM2 label missing for {image_file}: {label_file}')

        with open(label_file, encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
        if not lines:
            raise ValueError(f'MEDSAM2 label is empty: {label_file}')

        for line_number, line in enumerate(lines, start=1):
            parts = line.split()
            num_coords = len(parts) - 1
            if num_coords == 4:
                self._validate_bbox(parts, label_file, line_number)
            elif num_coords >= 6 and num_coords % 2 == 0:
                self._validate_polygon(parts, label_file, line_number)
            else:
                raise ValueError(
                    f'Invalid YOLO annotation in {label_file} line {line_number}: '
                    f'expected 5 values (bbox) or 6+ even values (polygon)'
                )

    def _validate_bbox(self, parts: list[str], label_file: str, line_number: int) -> None:
        class_index = int(parts[0])
        x, y, width, height = (float(value) for value in parts[1:])
        if class_index < 0:
            raise ValueError(f'Invalid class index in {label_file} line {line_number}')
        if not all(0.0 <= value <= 1.0 for value in (x, y, width, height)):
            raise ValueError(f'YOLO bbox values must be between 0 and 1 in {label_file} line {line_number}')
        if width == 0.0 or height == 0.0:
            raise ValueError(
                f'YOLO bbox width and height must be greater than zero in {label_file} line {line_number}'
            )
        if x - width / 2.0 < 0.0 or y - height / 2.0 < 0.0 or x + width / 2.0 > 1.0 or y + height / 2.0 > 1.0:
            raise ValueError(f'YOLO bbox must remain within image bounds in {label_file} line {line_number}')

    def _validate_polygon(self, parts: list[str], label_file: str, line_number: int) -> None:
        class_index = int(parts[0])
        coords = [float(value) for value in parts[1:]]
        if class_index < 0:
            raise ValueError(f'Invalid class index in {label_file} line {line_number}')
        if not all(0.0 <= value <= 1.0 for value in coords):
            raise ValueError(f'YOLO polygon values must be between 0 and 1 in {label_file} line {line_number}')
