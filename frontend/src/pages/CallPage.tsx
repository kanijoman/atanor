import { useEffect, useState } from "react";

type Call = {
  id: string;
  title: string;
};

type Programme = {
  id: string;
  identifier: string;
  title: string;
};

type CallPageProps = {
  callId: string;
};

export function CallPage({ callId }: CallPageProps) {
  const [call, setCall] = useState<Call | null>(null);
  const [programmes, setProgrammes] = useState<Programme[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError(false);

    Promise.all([
      fetch(`/api/calls/${callId}`),
      fetch(`/api/calls/${callId}/programmes`),
    ])
      .then(async ([callResponse, programmesResponse]) => {
        if (!callResponse.ok || !programmesResponse.ok) {
          throw new Error("Unable to load call");
        }

        const [callData, programmesData] = await Promise.all([
          callResponse.json() as Promise<Call>,
          programmesResponse.json() as Promise<Programme[]>,
        ]);

        return { call: callData, programmes: programmesData };
      })
      .then(({ call: callData, programmes: programmesData }) => {
        setCall(callData);
        setProgrammes(programmesData);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [callId]);

  return (
    <main>
      {loading && <p>Loading call…</p>}

      {!loading && error && <p>Unable to load call.</p>}

      {!loading && !error && call && (
        <>
          <h1>{call.title}</h1>

          {programmes.length === 0 ? (
            <p>No programmes are available for this call yet.</p>
          ) : (
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
        </>
      )}
    </main>
  );
}
