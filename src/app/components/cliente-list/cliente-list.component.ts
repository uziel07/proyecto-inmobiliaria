import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Cliente } from '../../models/cliente.model';
import { ClienteService } from '../../services/cliente.service';
import { ClienteFormComponent } from '../cliente-form/cliente-form.component';

@Component({ selector: 'app-cliente-list', standalone: true, imports: [FormsModule, ClienteFormComponent], templateUrl: './cliente-list.component.html' })
export class ClienteListComponent implements OnInit {
  private readonly service = inject(ClienteService);
  readonly clientes = signal<Cliente[]>([]);
  readonly cargando = signal(true);
  readonly error = signal('');
  readonly mensaje = signal('');
  readonly editandoId = signal<string | null>(null);
  readonly formEdicion = signal<{ nombre: string; email: string; documento: string; telefono: string } | null>(null);

  ngOnInit(): void { this.refrescar(); }

  refrescar(): void {
    this.cargando.set(this.clientes().length === 0);
    this.service.obtenerClientes().subscribe({ next: (data) => { this.clientes.set(data); this.cargando.set(false); this.error.set(''); }, error: () => { this.error.set('No se pudo conectar con la API.'); this.cargando.set(false); } });
  }

  eliminar(cliente: Cliente): void {
    if (!confirm(`¿Eliminar al cliente "${cliente.usuario?.nombre ?? cliente.documento}"?`)) { return; }
    this.service.eliminarCliente(cliente.id).subscribe({ next: () => { this.clientes.update((items) => items.filter((item) => item.id !== cliente.id)); this.mensaje.set('Cliente eliminado.'); window.setTimeout(() => this.mensaje.set(''), 3000); }, error: (response: HttpErrorResponse) => { this.error.set(response.error?.detail ?? 'No se pudo eliminar el cliente.'); } });
  }

  empezarEdicion(cliente: Cliente): void {
    this.editandoId.set(cliente.id);
    this.formEdicion.set({ nombre: cliente.usuario?.nombre ?? '', email: cliente.usuario?.email ?? '', documento: cliente.documento, telefono: cliente.telefono ?? '' });
  }

  guardarEdicion(cliente: Cliente, valores: { nombre: string; email: string; documento: string; telefono: string }): void {
    this.service.actualizarCliente(cliente.id, { nombre: valores.nombre, email: valores.email, documento: valores.documento, telefono: valores.telefono || null }).subscribe({ next: () => { this.mensaje.set('Cliente actualizado.'); window.setTimeout(() => this.mensaje.set(''), 3000); this.editandoId.set(null); this.formEdicion.set(null); this.refrescar(); }, error: (response: HttpErrorResponse) => { this.error.set(response.error?.detail ?? 'No se pudo actualizar el cliente.'); } });
  }

  cancelarEdicion(): void { this.editandoId.set(null); this.formEdicion.set(null); }
}
