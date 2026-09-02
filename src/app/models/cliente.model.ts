export interface Usuario { id: string; email: string; nombre: string; activo: boolean; }
export interface Cliente { id: string; usuario_id: string | null; documento: string; telefono: string | null; usuario: Usuario | null; }
export interface ClienteCreate { email: string; nombre: string; documento: string; telefono: string | null; }
export interface ClienteUpdate { nombre?: string; email?: string; documento?: string; telefono?: string | null; activo?: boolean; }
