import type { ActionResult } from "../types/ActionResult";
import type { ImageUrlResponse } from "../types/ImageUrlResponse";
import type { ItemListResponse } from "../types/ItemListResponse";
import type { PipelineStatusResponse } from "../types/PipelineStatusResponse";

const BASE_URL = "/api";
const LICENSE_STORAGE_KEY = "licenseToken";

function getLicenseToken(): string | null {
  return localStorage.getItem(LICENSE_STORAGE_KEY);
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getLicenseToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["X-License-Token"] = token;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    headers,
    ...options,
  });

  if (response.status === 401 || response.status === 403) {
    localStorage.removeItem(LICENSE_STORAGE_KEY);
    window.location.reload();
    throw new Error("License invalid or expired");
  }

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  getItems: () => request<ItemListResponse>("/items"),
  getItemImage: (itemId: string) => request<ImageUrlResponse>(`/items/${itemId}/image`),
  getPipelineStatus: () => request<PipelineStatusResponse>("/pipeline/status"),
  acceptItem: () => request<ActionResult>("/pipeline/accept", { method: "POST" }),
  rejectItem: () => request<ActionResult>("/pipeline/reject", { method: "POST" }),
  skipItem: () => request<ActionResult>("/pipeline/skip", { method: "POST" }),
  goBack: () => request<ActionResult>("/pipeline/back", { method: "POST" }),
};
