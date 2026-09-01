import { ChangeDetectionStrategy, Component, computed, inject, OnInit, output, signal } from '@angular/core';
import { Producto, Categoria } from '../../models/producto.model';
import { ProductoService } from '../../services/producto.service';
import { PropertyCardComponent } from '../property-card/property-card.component';
@Component({ selector:'app-producto-list', standalone:true, imports:[PropertyCardComponent], templateUrl:'./producto-list.component.html', styleUrl:'./producto-list.component.scss', changeDetection:ChangeDetectionStrategy.OnPush })
export class ProductoListComponent implements OnInit {
  private readonly service = inject(ProductoService); readonly productoSeleccionado = output<void>();
  readonly productos = signal<Producto[]>([]); readonly cargando = signal(true); readonly error = signal(false); readonly categoriaSeleccionada = signal('Todas');
  readonly categorias = computed<Categoria[]>(() => [{id:'all',nombre:'Todas'}, ...this.productos().map((p) => p.categoria).filter((c, i, all) => all.findIndex((item) => item.id === c.id) === i)]);
  readonly productosFiltrados = computed(() => this.categoriaSeleccionada() === 'Todas' ? this.productos() : this.productos().filter((p) => p.categoria.nombre === this.categoriaSeleccionada()));
  ngOnInit(): void { this.service.obtenerProductos().subscribe({ next:(data) => { this.productos.set(data); this.cargando.set(false); }, error:() => { this.error.set(true); this.cargando.set(false); } }); }
  seleccionar(nombre:string): void { this.productoSeleccionado.emit(); }
}
