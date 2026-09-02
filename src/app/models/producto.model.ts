export interface Categoria { id: string; nombre: string; slug: string; }
export type EstadoProducto = 'disponible' | 'en_oferta' | 'alquilada' | 'reservada';
export interface Producto { id: string; nombre: string; descripcion: string; ubicacion: string; sku: string; precio: number; rentabilidad_estimada: number; stock: number; imagen_url: string; estado: EstadoProducto; activo: boolean; categoria: Categoria; }
export interface ProductoCreate { categoria_id: string; nombre: string; descripcion: string; ubicacion: string; sku: string; precio: number; rentabilidad_estimada: number; stock: number; imagen_url: string; estado: EstadoProducto; activo: boolean; }
