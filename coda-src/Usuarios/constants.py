TUTOR = "TUT"
COORDINADOR = "COR"
ALUMNO = "ALU"

ROLES = [
    (TUTOR, "Tutor"),
    (COORDINADOR, "Coordinador"),
    (ALUMNO, "Alumno"),
]


MATEMATICAS = "MAT"
COMPUTACION = "COM"

CARRERAS = [
        (MATEMATICAS, "Matemáticas Aplicadas"),
        (COMPUTACION, "Ingeniería en Computación"),
    ]

TEMPLATES = {
    # ALUMNO: 'Usuarios/HeaderFooterAlumno.html',
    # TUTOR: 'Usuarios/HeaderFooterTutor.html',
    # COORDINADOR: 'Usuarios/HeaderFooterCoord.html',
    ALUMNO: 'Usuarios/navbar_alumno.html',
    TUTOR: 'Usuarios/navbar_tutor.html',
    COORDINADOR: 'Usuarios/navbar_coord.html',
}

CORREO = 'tutorias.beta.uamc@gmail.com'