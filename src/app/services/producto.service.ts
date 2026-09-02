import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { environment } from '../../environments/environment';
import { Categoria, Producto, ProductoCreate } from '../models/producto.model';

@Injectable({ providedIn:'root' })
export class ProductoService {
  private readonly http = inject(HttpClient);
  obtenerProductos() { return this.http.get<Producto[]>(`${environment.apiUrl}/productos`); }
  obtenerCategorias() { return this.http.get<Categoria[]>(`${environment.apiUrl}/categorias`); }
  crearProducto(producto: ProductoCreate) { return this.http.post<Producto>(`${environment.apiUrl}/productos`, producto); }
}
