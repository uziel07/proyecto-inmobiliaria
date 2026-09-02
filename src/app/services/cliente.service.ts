import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { environment } from '../../environments/environment';
import { Cliente, ClienteCreate, ClienteUpdate } from '../models/cliente.model';

@Injectable({ providedIn:'root' })
export class ClienteService {
  private readonly http = inject(HttpClient);
  obtenerClientes() { return this.http.get<Cliente[]>(`${environment.apiUrl}/clientes`); }
  obtenerCliente(id: string) { return this.http.get<Cliente>(`${environment.apiUrl}/clientes/${id}`); }
  crearCliente(cliente: ClienteCreate) { return this.http.post<Cliente>(`${environment.apiUrl}/clientes`, cliente); }
  actualizarCliente(id: string, cliente: ClienteUpdate) { return this.http.put<Cliente>(`${environment.apiUrl}/clientes/${id}`, cliente); }
  eliminarCliente(id: string) { return this.http.delete<void>(`${environment.apiUrl}/clientes/${id}`); }
}
