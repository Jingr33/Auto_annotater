export const ImagePredictionStatus = {
  Pending: "pending",
  Accepted: "accepted",
  Rejected: "rejected",
} as const;

export type ImagePredictionStatus =
  (typeof ImagePredictionStatus)[keyof typeof ImagePredictionStatus];
