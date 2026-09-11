import { ProgrammePage } from "./pages/ProgrammePage";
import { ProgrammesPage } from "./pages/ProgrammesPage";

type Route =
  | { name: "programmes" }
  | { name: "programme"; programmeId: string }
  | { name: "study"; unitId: string }
  | { name: "not-found" };

export function resolveRoute(pathname: string): Route {
  const segments = pathname.split("/").filter(Boolean);

  if (segments.length === 1 && segments[0] === "programmes") {
    return { name: "programmes" };
  }

  if (segments.length === 2 && segments[0] === "programmes") {
    return { name: "programme", programmeId: segments[1] };
  }

  if (segments.length === 2 && segments[0] === "study") {
    return { name: "study", unitId: segments[1] };
  }

  return { name: "not-found" };
}

function StudyPage({ unitId }: { unitId: string }) {
  return (
    <main>
      <h1>Study</h1>
      <p>Study material for programme unit {unitId} is not available yet.</p>
    </main>
  );
}

function NotFoundPage() {
  return (
    <main>
      <h1>Page not found</h1>
    </main>
  );
}

export function App() {
  const route = resolveRoute(window.location.pathname);

  switch (route.name) {
    case "programmes":
      return <ProgrammesPage />;
    case "programme":
      return <ProgrammePage programmeId={route.programmeId} />;
    case "study":
      return <StudyPage unitId={route.unitId} />;
    case "not-found":
      return <NotFoundPage />;
  }
}
