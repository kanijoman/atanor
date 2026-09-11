import { useEffect, useState } from "react";

type Programme = {
  id: string;
  identifier: string;
  title: string;
};

export function ProgrammesPage() {
  const [programmes, setProgrammes] = useState<Programme[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("/api/study/programmes")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to load programmes");
        }
        return response.json() as Promise<Programme[]>;
      })
      .then(setProgrammes)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main>
      <h1>Programmes</h1>

      {loading && <p>Loading programmes…</p>}

      {!loading && error && <p>Unable to load programmes.</p>}

      {!loading && !error && programmes.length === 0 && (
        <p>No programmes are available yet.</p>
      )}

      {!loading && !error && programmes.length > 0 && (
        <ul>
          {programmes.map((programme) => (
            <li key={programme.id}>
              <a href={`/programmes/${programme.id}`}>
                {programme.identifier} — {programme.title}
              </a>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
