export interface Categoria { id: string; nombre: string; }
export type EstadoProducto = 'Disponible' | 'En oferta' | 'Alquilada' | 'Reservada';
export interface Producto { id: string; nombre: string; descripcion: string; ubicacion: string; sku: string; precio: number; rentabilidad_estimada: number; imagen_url: string; estado: EstadoProducto; activo: boolean; categoria: Categoria; }
