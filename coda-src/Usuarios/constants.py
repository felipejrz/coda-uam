TUTOR = "TUT"
COORDINADOR = "COR"
ALUMNO = "ALU"
CODA = "CODA"

ROLES = [
    ('', "Seleccione Rol"),
    (TUTOR, "Tutor"),
    (COORDINADOR, "Coordinador"),
    (ALUMNO, "Alumno"),
    (CODA, "Coda"),
]


MATEMATICAS = "MAT"
COMPUTACION = "COM"

CARRERAS = [
        ('', "Seleccione una"),
        (MATEMATICAS, "Matemáticas Aplicadas"),
        (COMPUTACION, "Ingeniería en Computación"),
    ]

TEMPLATES = {
    # ALUMNO: 'Usuarios/HeaderFooterAlumno.html',
    # TUTOR: 'Usuarios/HeaderFooterTutor.html',
    # COORDINADOR: 'Usuarios/HeaderFooterCoord.html',
    ALUMNO: 'Usuarios/navbar_alumno.html',
    TUTOR: 'Usuarios/navbar_tutor.html',
    COORDINADOR: 'Usuarios/navbar_tutor.html',
    CODA: 'Usuarios/navbar_tutor.html',
}

CORREO = 'tutorias.beta.uamc@gmail.com'