"""Seed catalog of the laws that public-service syllabi most often rely on.

It is curated data, reusable across calls: each law has the designation it is cited by and the
phrases that, when a syllabus unit uses them, point to that law. It is not generated and it is
deliberately small; a law outside it is found only through an explicit reference (BOE lookup).
"""

from dataclasses import dataclass

from app.application.normative_source import (
    CONSTITUCION_ESPANOLA,
    LEY_7_1985,
    LEY_19_2013,
    LEY_29_1998,
    LEY_39_2015,
    LEY_40_2015,
    LEY_47_2003,
    LEY_50_1997,
    RDL_4_2000,
    TREBEP,
    NormativeSourceCandidate,
)
from app.domain.models import Source


@dataclass(frozen=True)
class SeedLaw:
    candidate: NormativeSourceCandidate
    designation: str  # accent-free, lower case: "ley organica 6/1985"
    keywords: tuple[str, ...]  # accent-free, lower case phrases that name the subject


def _candidate(identifier: str, title: str, label: str) -> NormativeSourceCandidate:
    locator = f"https://www.boe.es/buscar/act.php?id={identifier}"
    return NormativeSourceCandidate(
        source=Source(title=title, locator=locator),
        authority="BOE",
        identifier=identifier,
        label=label,
    )


_LOPJ = _candidate("BOE-A-1985-12666", "Ley Orgánica 6/1985, del Poder Judicial", "LO 6/1985")
_LOTC = _candidate(
    "BOE-A-1979-23709", "Ley Orgánica 2/1979, del Tribunal Constitucional", "LO 2/1979"
)
_DEFENSOR = _candidate(
    "BOE-A-1981-10325", "Ley Orgánica 3/1981, del Defensor del Pueblo", "LO 3/1981"
)
_LOPDGDD = _candidate(
    "BOE-A-2018-16673",
    "Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales",
    "LO 3/2018",
)
_LCSP = _candidate("BOE-A-2017-12902", "Ley 9/2017, de Contratos del Sector Público", "Ley 9/2017")
_INCOMPATIBILIDADES = _candidate(
    "BOE-A-1985-151",
    "Ley 53/1984, de Incompatibilidades del personal al servicio de las Administraciones Públicas",
    "Ley 53/1984",
)
_IGUALDAD = _candidate(
    "BOE-A-2007-6115",
    "Ley Orgánica 3/2007, para la igualdad efectiva de mujeres y hombres",
    "LO 3/2007",
)
_VIOLENCIA_GENERO = _candidate(
    "BOE-A-2004-21760",
    "Ley Orgánica 1/2004, de Medidas de Protección Integral contra la Violencia de Género",
    "LO 1/2004",
)
_IGUALDAD_TRATO = _candidate(
    "BOE-A-2022-11589",
    "Ley 15/2022, integral para la igualdad de trato y la no discriminación",
    "Ley 15/2022",
)
_LGTBI = _candidate(
    "BOE-A-2023-5366",
    "Ley 4/2023, para la igualdad real y efectiva de las personas trans y para la garantía "
    "de los derechos de las personas LGTBI",
    "Ley 4/2023",
)
_DISCAPACIDAD = _candidate(
    "BOE-A-2013-12632",
    "Real Decreto Legislativo 1/2013, Ley General de derechos de las personas con "
    "discapacidad y de su inclusión social",
    "RDL 1/2013",
)
_DEPENDENCIA = _candidate(
    "BOE-A-2006-21990",
    "Ley 39/2006, de Promoción de la Autonomía Personal y Atención a las personas en "
    "situación de dependencia",
    "Ley 39/2006",
)

SEED_LAWS: tuple[SeedLaw, ...] = (
    SeedLaw(
        CONSTITUCION_ESPANOLA,
        "constitucion espanola",
        (
            "constitucion",
            "corona",
            "cortes generales",
            "presidente del gobierno",
            "poder judicial",
            "derechos y deberes fundamentales",
            "presupuesto del estado",
        ),
    ),
    SeedLaw(
        LEY_50_1997,
        "ley 50/1997",
        ("el gobierno y la administracion", "presidente del gobierno", "consejo de ministros"),
    ),
    SeedLaw(
        LEY_40_2015,
        "ley 40/2015",
        ("regimen juridico del sector publico", "administracion general del estado"),
    ),
    SeedLaw(
        LEY_39_2015,
        "ley 39/2015",
        ("procedimiento administrativo comun", "recursos administrativos"),
    ),
    SeedLaw(
        LEY_7_1985,
        "ley 7/1985",
        ("administracion local", "la provincia, el municipio", "regimen local"),
    ),
    SeedLaw(
        LEY_19_2013,
        "ley 19/2013",
        ("transparencia", "acceso a la informacion publica", "buen gobierno"),
    ),
    SeedLaw(LEY_29_1998, "ley 29/1998", ("contencioso-administrativo", "jurisdiccion contencioso")),
    SeedLaw(LEY_47_2003, "ley 47/2003", ("presupuesto del estado", "ciclo presupuestario")),
    SeedLaw(
        TREBEP,
        "real decreto legislativo 5/2015",
        (
            "estatuto basico del empleado publico",
            "personal funcionario",
            "funcionarios",
            "carrera administrativa",
            "regimen disciplinario",
        ),
    ),
    SeedLaw(
        RDL_4_2000, "real decreto legislativo 4/2000", ("seguridad social de los funcionarios",)
    ),
    SeedLaw(_LOPJ, "ley organica 6/1985", ("poder judicial", "organizacion judicial")),
    SeedLaw(_LOTC, "ley organica 2/1979", ("tribunal constitucional",)),
    SeedLaw(_DEFENSOR, "ley organica 3/1981", ("defensor del pueblo",)),
    SeedLaw(
        _LOPDGDD, "ley organica 3/2018", ("proteccion de datos personales", "derechos digitales")
    ),
    SeedLaw(_LCSP, "ley 9/2017", ("contratos del sector publico",)),
    SeedLaw(_INCOMPATIBILIDADES, "ley 53/1984", ("incompatibilidades",)),
    SeedLaw(_IGUALDAD, "ley organica 3/2007", ("politicas de igualdad", "igualdad efectiva")),
    SeedLaw(_VIOLENCIA_GENERO, "ley organica 1/2004", ("violencia de genero",)),
    SeedLaw(_IGUALDAD_TRATO, "ley 15/2022", ("igualdad de trato", "no discriminacion")),
    SeedLaw(_LGTBI, "ley 4/2023", ("lgtbi",)),
    SeedLaw(_DISCAPACIDAD, "real decreto legislativo 1/2013", ("discapacidad y dependencia",)),
    SeedLaw(_DEPENDENCIA, "ley 39/2006", ("dependencia",)),
)
