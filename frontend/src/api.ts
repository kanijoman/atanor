export type Call = {
  id: string;
  title: string;
};

export type CallProgramme = {
  id: string;
  identifier: string;
  title: string;
};

export type ProgrammeUnit = {
  id: string;
  number: number;
  title: string;
  study_material_available: boolean;
};

export type Programme = {
  identifier: string;
  title: string;
  units: ProgrammeUnit[];
};

export type StudyCoverage = {
  status: "missing" | "partial" | "covered";
  covered_count: number;
  required_count: number;
  coverage_percentage: number;
  required_aspects: string[];
  covered_aspects: string[];
  pending_aspects: string[];
};

export type StudySource = {
  title: string;
  locator: string | null;
};

export type MaterialProvenance = {
  origin: "curated" | "acquired";
  review_status: "unreviewed" | "reviewed";
};

export type StudyResponse = {
  programme_unit: {
    id: string;
    number: number;
    title: string;
  };
  knowledge_need: {
    title: string;
  };
  provenance: MaterialProvenance;
  study_material: string;
  sources: StudySource[];
  coverage: StudyCoverage;
};

export class ApiError extends Error {
  constructor(
    readonly status: number,
    path: string,
  ) {
    super(`Request to ${path} failed with status ${status}`);
  }
}

export async function fetchJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(path, { signal });

  if (!response.ok) {
    throw new ApiError(response.status, path);
  }

  return (await response.json()) as T;
}
