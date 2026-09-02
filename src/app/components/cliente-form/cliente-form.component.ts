import { ChangeDetectionStrategy, Component, inject, output, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { ClienteCreate } from '../../models/cliente.model';
import { ClienteService } from '../../services/cliente.service';

@Component({ selector: 'app-cliente-form', standalone: true, imports: [ReactiveFormsModule], templateUrl: './cliente-form.component.html', styleUrl: './cliente-form.component.scss', changeDetection: ChangeDetectionStrategy.OnPush })
export class ClienteFormComponent {
  private readonly fb = inject(NonNullableFormBuilder);
  private readonly service = inject(ClienteService);
  readonly clienteCreado = output<void>();
  readonly enviando = signal(false);
  readonly mensaje = signal('');
  readonly error = signal('');
  readonly form = this.fb.group({ nombre: ['', [Validators.required, Validators.minLength(2)]], email: ['', [Validators.required, Validators.email]], documento: ['', [Validators.required, Validators.minLength(3)]], telefono: [''] });

  guardar(): void {
    if (this.form.invalid || this.enviando()) { this.form.markAllAsTouched(); return; }
    this.enviando.set(true); this.mensaje.set(''); this.error.set('');
    const payload: ClienteCreate = {
      nombre: this.form.getRawValue().nombre,
      email: this.form.getRawValue().email,
      documento: this.form.getRawValue().documento,
      telefono: this.form.getRawValue().telefono || null,
    };
    this.service.crearCliente(payload).subscribe({ next: () => { this.mensaje.set('Cliente registrado correctamente.'); this.form.reset({ nombre: '', email: '', documento: '', telefono: '' }); this.enviando.set(false); this.clienteCreado.emit(); }, error: (response: HttpErrorResponse) => { this.error.set(response.error?.detail ?? 'No se pudo registrar el cliente.'); this.enviando.set(false); } });
  }
}
