from routers import tipo_programa, programa, programa_version, modulo, modalidad_academica, modalidad, programa_version_edicion, docente, detalle_programa_modulo

all_routers = [
    tipo_programa.router,
    programa.router,
    programa_version.router,
    modulo.router,
    modalidad_academica.router,
    modalidad.router,
    programa_version_edicion.router,
    docente.router,
    detalle_programa_modulo.router,
]