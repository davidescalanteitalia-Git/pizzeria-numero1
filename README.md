# Pizzeria Numero 1

Web de la pizzeria d'asporto y kebab **Numero 1**, Via Bellinzona 187,
Monte Olimpino, Como.

- **Produccion:** https://pizzerianumero1.d4digitalstudio.it
- **Provisional:** https://pizzerianumero1.pages.dev

Razon social: Pizzeria Noi Tre di Zoheir Abir Sayed Ali A. · P.IVA 04221150131

---

## Como se publica

Cada `git push` a la rama `main` publica sola la web en Cloudflare Pages,
mediante el flujo de `.github/workflows/deploy.yml`.

Para que funcione hacen falta dos secretos en el repositorio
(Settings › Secrets and variables › Actions › New repository secret):

| Nombre | De donde sale |
|---|---|
| `CLOUDFLARE_API_TOKEN` | dash.cloudflare.com › My Profile › API Tokens › Create Token › plantilla "Edit Cloudflare Workers" |
| `CLOUDFLARE_ACCOUNT_ID` | dash.cloudflare.com, en la barra lateral de la cuenta |

## Que hay dentro

| Archivo | Que es |
|---|---|
| `index.html` | La pagina entera, sin dependencias externas |
| `privacy.html` | Informativa privacy en italiano, obligatoria |
| `manifest.webmanifest` · `sw.js` | La convierten en app instalable y sin conexion |
| `mappa.jpg` | Mapa propio hecho con datos de OpenStreetMap |
| `th-*.jpg` | Miniaturas de las pizzas en la carta |
| `foto-*.jpg` | Fotos grandes de portada |
| `ill-*.svg` | Ilustraciones de marca, de reserva |
| `robots.txt` · `sitemap.xml` | Para Google |
| `LEEME.txt` · `PUBLICAR.txt` | Notas de mantenimiento |

## Reglas de la casa

- **Sin terceros.** La pagina no carga nada de fuera: ni Google Fonts, ni
  Analytics, ni mapas incrustados. Por eso no necesita banner de cookies.
  Si algun dia se añade algo externo, hay que actualizar `privacy.html`
  y poner banner de consentimiento.
- **Al añadir un archivo nuevo**, apuntarlo tambien en la lista de `sw.js`
  y subir el numero de version de la cache, o no se vera sin conexion.
- **Las fotos** no son de Numero 1, son genericas. Sustituirlas en cuanto
  el propietario mande las suyas. Cuidado con que los ingredientes que se
  ven coincidan con el texto (Reg. UE 1169/2011, art. 7).
- **Los precios** salen del folleto: 6,99 € pizza mas bebida, hasta el
  31 de diciembre de 2026. Si cambia la oferta, cambiar tambien la cabecera.

## Pendiente antes de dar por buena la web

Ver `PUBLICAR.txt`. En resumen: correo real para la privacy, carta de kebab
y piadine, zona de reparto, y fotos del horno de leña y del kebab.
