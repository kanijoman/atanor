import { useEffect, useState } from "react";

type ProgrammeUnit = {
  id: string;
  number: number;
  title: string;
};

type Programme = {
  identifier: string;
  title: string;
  units: ProgrammeUnit[];
};

type ProgrammePageProps = {
  programmeId: string;
};

export function ProgrammePage({ programmeId }: ProgrammePageProps) {
  const [programme, setProgramme] = useState<Programme | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`/api/study/programmes/${programmeId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load programme");
        }
        return response.json() as Promise<Programme>;
      })
      .then(setProgramme)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [programmeId]);

  return (
    <main>
      {loading && <p>Loading programme…</p>}

      {!loading && error && <p>Unable to load programme.</p>}

      {!loading && !error && programme && (
        <>
          <h1>Programme {programme.identifier}</h1>
          <p>{programme.title}</p>

          {programme.units.length === 0 ? (
            <p>No programme units are available yet.</p>
          ) : (
            <ul>
              {programme.units.map((unit) => (
                <li key={unit.id}>
                  <a href={`/study/${unit.id}`}>
                    {unit.number}. {unit.title}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </main>
  );
}
