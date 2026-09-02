from backend.annotations.bbox_annotation import BBoxAnnotation
from backend.annotations.polygon_annotation import PolygonAnnotation


class PolygonToBboxConverter:
    @staticmethod
    def convert(polygon: PolygonAnnotation) -> BBoxAnnotation:
        if not polygon.points:
            return BBoxAnnotation(
                class_index=polygon.class_index,
                x=0.0,
                y=0.0,
                width=0.0,
                height=0.0,
            )

        x_coords = [p[0] for p in polygon.points]
        y_coords = [p[1] for p in polygon.points]

        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)

        return BBoxAnnotation(
            class_index=polygon.class_index,
            x=min_x,
            y=min_y,
            width=max_x - min_x,
            height=max_y - min_y,
        )
