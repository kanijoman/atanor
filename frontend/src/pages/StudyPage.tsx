import { useEffect, useState } from "react";

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
};

type StudyPageProps = {
  unitId: string;
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
          <div style={{ whiteSpace: "pre-wrap" }}>{study.study_material}</div>
        </>
      )}
    </main>
  );
}
