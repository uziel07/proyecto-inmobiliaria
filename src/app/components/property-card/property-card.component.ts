import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { Producto } from '../../models/producto.model';
@Component({ selector:'app-property-card', standalone:true, imports:[CurrencyPipe], templateUrl:'./property-card.component.html', changeDetection:ChangeDetectionStrategy.OnPush })
export class PropertyCardComponent {
  readonly producto = input.required<Producto>();
  readonly seleccionar = output<Producto>();
  readonly verPropiedad = output<Producto>();
  mostrarEstado(estado: Producto['estado']): string { return estado.replace('_', ' '); }
  imagenFallida(event: Event): void { const image = event.target as HTMLImageElement; image.src = '/images/properties/property-placeholder.svg'; }
}
