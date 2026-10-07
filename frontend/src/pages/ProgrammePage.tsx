import { type Programme, type ProgrammeUnit, fetchJson } from "../api";
import { useApi } from "../useApi";

type ProgrammePageProps = {
  programmeId: string;
};

type UnitGroup = { section: string | null; units: ProgrammeUnit[] };

/** Groups consecutive units by block; programmes may restart numbering in each block. */
function groupBySection(units: ProgrammeUnit[]): UnitGroup[] {
  const groups: UnitGroup[] = [];
  for (const unit of units) {
    const last = groups.at(-1);
    if (last && last.section === unit.section) {
      last.units.push(unit);
    } else {
      groups.push({ section: unit.section, units: [unit] });
    }
  }
  return groups;
}

function UnitItem({ unit }: { unit: ProgrammeUnit }) {
  const label = (
    <>
      {unit.number}. {unit.title}
    </>
  );

  return (
    <li>
      {unit.study_material_available ? (
        <a href={`/study/${unit.id}`}>{label}</a>
      ) : (
        <span>{label}</span>
      )}
      <span>
        {unit.study_material_available
          ? "Study material available"
          : "Study material not available"}
      </span>
    </li>
  );
}

function UnitGroupList({ group }: { group: UnitGroup }) {
  return (
    <section>
      {group.section && <h2>{group.section}</h2>}
      <ul>
        {group.units.map((unit) => (
          <UnitItem key={unit.id} unit={unit} />
        ))}
      </ul>
    </section>
  );
}

export function ProgrammePage({ programmeId }: ProgrammePageProps) {
  const state = useApi(programmeId, (signal) =>
    fetchJson<Programme>(`/api/study/programmes/${programmeId}`, signal),
  );

  return (
    <main>
      {state.status === "loading" && <p>Loading programme…</p>}

      {state.status === "error" && <p>Unable to load programme.</p>}

      {state.status === "ready" && (
        <>
          <h1>Programme {state.data.identifier}</h1>
          <p>{state.data.title}</p>
          <p>
            {state.data.coverage.units_with_material} of {state.data.coverage.units_total} units
            have study material
          </p>

          {state.data.units.length === 0 ? (
            <p>No programme units are available yet.</p>
          ) : (
            groupBySection(state.data.units).map((group) => (
              <UnitGroupList key={`${group.section}-${group.units[0].id}`} group={group} />
            ))
          )}
        </>
      )}
    </main>
  );
}
