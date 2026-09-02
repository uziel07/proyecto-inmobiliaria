import { ChangeDetectionStrategy, Component, inject, OnInit, output, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Categoria, EstadoProducto, ProductoCreate } from '../../models/producto.model';
import { ProductoService } from '../../services/producto.service';

@Component({ selector: 'app-property-form', standalone: true, imports: [ReactiveFormsModule], templateUrl: './property-form.component.html', styleUrl: './property-form.component.scss', changeDetection: ChangeDetectionStrategy.OnPush })
export class PropertyFormComponent implements OnInit {
  private readonly fb = inject(NonNullableFormBuilder);
  private readonly service = inject(ProductoService);
  readonly productoCreado = output<void>();
  readonly categorias = signal<Categoria[]>([]);
  readonly enviando = signal(false);
  readonly mensaje = signal('');
  readonly error = signal('');
  readonly estados: EstadoProducto[] = ['disponible', 'en_oferta', 'alquilada', 'reservada'];
  readonly form = this.fb.group({ categoria_id: ['', Validators.required], nombre: ['', [Validators.required, Validators.minLength(2)]], descripcion: ['', [Validators.required, Validators.minLength(10)]], ubicacion: ['', Validators.required], sku: ['', Validators.required], precio: [0, [Validators.required, Validators.min(1)]], rentabilidad_estimada: [0, [Validators.required, Validators.min(0), Validators.max(100)]], stock: [1, [Validators.required, Validators.min(0)]], imagen_url: ['/images/properties/property-placeholder.svg'], estado: ['disponible' as EstadoProducto, Validators.required], activo: [true] });

  ngOnInit(): void { this.service.obtenerCategorias().subscribe({ next: (data) => this.categorias.set(data) }); }

  guardar(): void {
    if (this.form.invalid || this.enviando()) { this.form.markAllAsTouched(); return; }
    this.enviando.set(true); this.mensaje.set(''); this.error.set('');
    this.service.crearProducto(this.form.getRawValue() as ProductoCreate).subscribe({ next: () => { this.mensaje.set('Propiedad registrada correctamente.'); this.form.reset({ categoria_id: '', nombre: '', descripcion: '', ubicacion: '', sku: '', precio: 0, rentabilidad_estimada: 0, stock: 1, imagen_url: '/images/properties/property-placeholder.svg', estado: 'disponible', activo: true }); this.enviando.set(false); this.productoCreado.emit(); }, error: (response: HttpErrorResponse) => { this.error.set(response.error?.detail ?? 'No se pudo registrar la propiedad.'); this.enviando.set(false); } });
  }
}
