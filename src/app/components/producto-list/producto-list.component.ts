import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject, OnDestroy, OnInit, output, signal } from '@angular/core';
import { Subscription, timer } from 'rxjs';
import { exhaustMap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { Producto, Categoria } from '../../models/producto.model';
import { ProductoService } from '../../services/producto.service';
import { PropertyCardComponent } from '../property-card/property-card.component';
import { PropertyFormComponent } from '../property-form/property-form.component';
import { PropertyDetailComponent } from '../property-detail/property-detail.component';

@Component({ selector: 'app-producto-list', standalone: true, imports: [DatePipe, PropertyCardComponent, PropertyFormComponent, PropertyDetailComponent], templateUrl: './producto-list.component.html', styleUrl: './producto-list.component.scss', changeDetection: ChangeDetectionStrategy.OnPush })
export class ProductoListComponent implements OnInit, OnDestroy {
  private readonly service = inject(ProductoService);
  private readonly polling = new Subscription();
  private ids = new Set<string>();
  readonly productoSeleccionado = output<Producto>();
  readonly productos = signal<Producto[]>([]);
  readonly categorias = signal<Categoria[]>([]);
  readonly cargando = signal(true);
  readonly error = signal('');
  readonly categoriaSeleccionada = signal('Todas');
  readonly estadoSeleccionado = signal('Todos');
  readonly ultimaActualizacion = signal<Date | null>(null);
  readonly aviso = signal('');
  readonly productosFiltrados = computed(() => this.productos().filter((producto) => (this.categoriaSeleccionada() === 'Todas' || producto.categoria.slug === this.categoriaSeleccionada()) && (this.estadoSeleccionado() === 'Todos' || producto.estado === this.estadoSeleccionado())));
  readonly productoDetalle = signal<Producto | null>(null);

  ngOnInit(): void {
    this.service.obtenerCategorias().subscribe({ next: (data) => this.categorias.set(data) });
    if (environment.autoRefreshProperties) {
      this.polling.add(timer(0, environment.refreshIntervalMs).pipe(exhaustMap(() => this.service.obtenerProductos())).subscribe({ next: (data) => this.actualizar(data), error: () => this.error.set('No se pudo conectar con la API.') }));
    } else {
      this.refrescar();
    }
  }

  ngOnDestroy(): void { this.polling.unsubscribe(); }

  refrescar(): void {
    this.cargando.set(this.productos().length === 0);
    this.service.obtenerProductos().subscribe({ next: (data) => this.actualizar(data), error: () => { this.error.set('No se pudo conectar con la API.'); this.cargando.set(false); } });
  }

  propiedadCreada(): void { this.refrescar(); }
  cambiarEstado(event: Event): void { this.estadoSeleccionado.set((event.target as HTMLSelectElement).value); }

  private actualizar(data: Producto[]): void {
    const nuevos = this.ids.size > 0 && data.some((producto) => !this.ids.has(producto.id));
    this.ids = new Set(data.map((producto) => producto.id));
    this.productos.set(data);
    this.cargando.set(false);
    this.error.set('');
    this.ultimaActualizacion.set(new Date());
    if (nuevos) { this.aviso.set('Nuevas propiedades disponibles'); window.setTimeout(() => this.aviso.set(''), 3500); }
  }

  seleccionar(producto: Producto): void { this.productoSeleccionado.emit(producto); }
  verDetalle(producto: Producto): void { this.productoDetalle.set(producto); }
  cerrarDetalle(): void { this.productoDetalle.set(null); }
}
