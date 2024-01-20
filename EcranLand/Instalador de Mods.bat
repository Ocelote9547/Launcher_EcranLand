@echo off

REM Establecer la ubicación del escritorio y AppData
set "escritorio1=%USERPROFILE%\OneDrive\Escritorio"
set "escritorio2=%USERPROFILE%\Escritorio"
set "escritorio3=%USERPROFILE%\OneDrive\DeskTop"
set "escritorio4=%USERPROFILE%\DeskTop"
set "appdata=%APPDATA%\ecranland"

REM Verificar si la carpeta .minecraft ya existe
if exist "%appdata%\ecranland" (
    echo La carpeta ecranland ya está instalada.
    exit /b 1
)

REM Crear una carpeta temporal para descargar los archivos necesarios
set "temp_folder=%TEMP%\Installers"
mkdir "%temp_folder%" 2>nul

REM URL del archivo que deseas descargar
set "download_url=https://bit.ly/EcranLanD"

REM Descargar desde la URL con Invoke-WebRequest
echo Descargando desde la URL...
powershell -Command "Invoke-WebRequest -Uri %download_url% -OutFile '%temp_folder%\ecranland.zip'"

REM Verificar si la descarga fue exitosa
if not exist "%temp_folder%\ecranland.zip" (
    echo No se pudo descargar el archivo desde la URL.
    pause
    exit /b 1
)

REM Esperar 3 segundos antes de descomprimir
timeout /nobreak /t 3 >nul

REM Descomprimir el archivo .zip y copiar a AppData
echo Extrayendo los mods del Zip
Expand-Archive -Path "%temp_folder%\ecranland.zip" -DestinationPath "%appdata%"

REM Eliminar el archivo .zip después de la instalación
del "%temp_folder%\ecranland.zip" 2>nul

REM Esperar 3 segundos antes de mostrar el mensaje de descarga completada
timeout /nobreak /t 3 >nul

REM Mostrar mensaje de descarga completada
echo Descarga de mods completada.
echo Presiona cualquier tecla para salir.
pause >nul
exit /b 0
