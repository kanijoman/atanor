import {
  type MaterialProvenance,
  type StudyCoverage,
  type StudyResponse,
  type StudySource,
  fetchJson,
} from "../api";
import { useApi } from "../useApi";

type StudyPageProps = {
  unitId: string;
};

const coverageStatusLabel: Record<StudyCoverage["status"], string> = {
  missing: "Missing",
  partial: "Partial",
  covered: "Covered",
};

const originLabel: Record<MaterialProvenance["origin"], string> = {
  curated: "Curated by Atanor",
  acquired: "Acquired from an authoritative source",
};

const reviewLabel: Record<MaterialProvenance["review_status"], string> = {
  unreviewed: "not yet reviewed by an expert",
  reviewed: "reviewed by an expert",
};

function CoverageSection({ coverage }: { coverage: StudyCoverage }) {
  return (
    <section aria-labelledby="study-coverage-heading">
      <h2 id="study-coverage-heading">Study coverage</h2>
      <p>
        {coverageStatusLabel[coverage.status]} · {coverage.covered_count} of{" "}
        {coverage.required_count} aspects covered ({coverage.coverage_percentage}%)
      </p>

      <h3>Study aspects</h3>
      <ul>
        {coverage.required_aspects.map((aspect) => (
          <li key={aspect}>
            <span>{coverage.covered_aspects.includes(aspect) ? "Covered" : "Pending"}</span> ·{" "}
            {aspect}
          </li>
        ))}
      </ul>
    </section>
  );
}

function MaterialSection({
  material,
  provenance,
}: {
  material: string;
  provenance: MaterialProvenance;
}) {
  return (
    <section aria-labelledby="study-material-heading">
      <h2 id="study-material-heading">Study material</h2>
      <p>
        {originLabel[provenance.origin]} · {reviewLabel[provenance.review_status]}
      </p>
      <div style={{ whiteSpace: "pre-wrap" }}>{material}</div>
    </section>
  );
}

function SourcesSection({ sources }: { sources: StudySource[] }) {
  return (
    <section aria-labelledby="study-sources-heading">
      <h2 id="study-sources-heading">Sources</h2>
      <ul>
        {sources.map((source) => (
          <li key={source.title}>
            {source.locator ? (
              <a href={source.locator} target="_blank" rel="noreferrer">
                {source.title}
              </a>
            ) : (
              <span>{source.title}</span>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function StudyPage({ unitId }: StudyPageProps) {
  const state = useApi(unitId, (signal) =>
    fetchJson<StudyResponse>(`/api/study/units/${unitId}`, signal),
  );
  const study = state.status === "ready" ? state.data : null;

  return (
    <main>
      {state.status === "loading" && <p>Loading study material…</p>}

      {state.status === "error" && <p>Unable to load study material.</p>}

      {study && (
        <>
          <h1>{study.programme_unit.title}</h1>
          <p>Knowledge need: {study.knowledge_need.title}</p>

          <CoverageSection coverage={study.coverage} />
          <MaterialSection material={study.study_material} provenance={study.provenance} />
          <SourcesSection sources={study.sources} />
        </>
      )}
    </main>
  );
}
