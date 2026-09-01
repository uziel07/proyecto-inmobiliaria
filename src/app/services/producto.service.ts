import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { catchError, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { Producto } from '../models/producto.model';

const demoProductos: Producto[] = [
  { id:'1', nombre:'Casa Lumen', descripcion:'Arquitectura serena y espacios abiertos.', ubicacion:'La Molina, Lima', sku:'NID-001', precio:485000, rentabilidad_estimada:8.4, imagen_url:'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=85', estado:'En oferta', activo:true, categoria:{id:'1',nombre:'Casas de lujo'} },
  { id:'2', nombre:'Atelier 48', descripcion:'Departamento urbano con demanda sostenida.', ubicacion:'Miraflores, Lima', sku:'NID-002', precio:212000, rentabilidad_estimada:7.8, imagen_url:'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1000&q=85', estado:'Disponible', activo:true, categoria:{id:'2',nombre:'Departamentos'} },
  { id:'3', nombre:'Patio Central', descripcion:'Local comercial en el corazón financiero.', ubicacion:'San Isidro, Lima', sku:'NID-003', precio:695000, rentabilidad_estimada:10.2, imagen_url:'https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1000&q=85', estado:'Disponible', activo:true, categoria:{id:'3',nombre:'Comercial'} },
  { id:'4', nombre:'Brisa Norte', descripcion:'Proyecto residencial con entrega 2027.', ubicacion:'Asia, Lima', sku:'NID-004', precio:178000, rentabilidad_estimada:9.1, imagen_url:'https://images.unsplash.com/photo-1600607688969-a5bfcd646154?auto=format&fit=crop&w=1000&q=85', estado:'Reservada', activo:true, categoria:{id:'4',nombre:'Preventa'} }
];

@Injectable({ providedIn:'root' })
export class ProductoService {
  private readonly http = inject(HttpClient);
  obtenerProductos() { return this.http.get<Producto[]>(`${environment.apiUrl}/productos`).pipe(catchError(() => of(demoProductos))); }
}
