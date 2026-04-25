/**
 * Fix Leaflet's default marker icons when bundled with Vite.
 * Vite's asset pipeline breaks Leaflet's auto-detection of the image path,
 * so we manually point to the correct assets.
 *
 * Import this module once, before any MapContainer is rendered.
 */
import L from 'leaflet';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

// Remove the broken built-in URL resolver
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl;

L.Icon.Default.mergeOptions({ iconUrl, iconRetinaUrl, shadowUrl });
