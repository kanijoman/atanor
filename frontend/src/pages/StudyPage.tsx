import { useEffect, useState } from "react";

type StudyCoverage = {
  status: "missing" | "partial" | "covered";
  covered_count: number;
  required_count: number;
  coverage_percentage: number;
  covered_aspects: string[];
  pending_aspects: string[];
};

type StudySource = {
  title: string;
  locator: string | null;
};

type StudyResponse = {
  programme_unit: {
    id: string;
    number: number;
    title: string;
  };
  knowledge_need: {
    title: string;
  };
  study_material: string;
  sources: StudySource[];
  coverage: StudyCoverage;
};

type StudyPageProps = {
  unitId: string;
};

const coverageStatusLabel: Record<StudyCoverage["status"], string> = {
  missing: "Missing",
  partial: "Partial",
  covered: "Covered",
};

export function StudyPage({ unitId }: StudyPageProps) {
  const [study, setStudy] = useState<StudyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`/api/study/units/${unitId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load study material");
        }
        return response.json() as Promise<StudyResponse>;
      })
      .then(setStudy)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [unitId]);

  return (
    <main>
      {loading && <p>Loading study material…</p>}

      {!loading && error && <p>Unable to load study material.</p>}

      {!loading && !error && study && (
        <>
          <h1>{study.programme_unit.title}</h1>
          <p>Knowledge need: {study.knowledge_need.title}</p>

          <section aria-labelledby="study-coverage-heading">
            <h2 id="study-coverage-heading">Study coverage</h2>
            <p>
              {coverageStatusLabel[study.coverage.status]} · {study.coverage.covered_count} of {study.coverage.required_count} aspects covered ({study.coverage.coverage_percentage}%)
            </p>

            {study.coverage.covered_aspects.length > 0 && (
              <>
                <h3>Covered aspects</h3>
                <ul>
                  {study.coverage.covered_aspects.map((aspect) => (
                    <li key={aspect}>{aspect}</li>
                  ))}
                </ul>
              </>
            )}

            {study.coverage.pending_aspects.length > 0 && (
              <>
                <h3>Pending aspects</h3>
                <ul>
                  {study.coverage.pending_aspects.map((aspect) => (
                    <li key={aspect}>{aspect}</li>
                  ))}
                </ul>
              </>
            )}
          </section>

          <section aria-labelledby="study-material-heading">
            <h2 id="study-material-heading">Study material</h2>
            <div style={{ whiteSpace: "pre-wrap" }}>{study.study_material}</div>
          </section>
        </>
      )}
    </main>
  );
}
