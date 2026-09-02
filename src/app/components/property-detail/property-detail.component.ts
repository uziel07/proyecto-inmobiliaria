import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { Producto } from '../../models/producto.model';

@Component({ selector: 'app-property-detail', standalone: true, imports: [CurrencyPipe], templateUrl: './property-detail.component.html', styleUrl: './property-detail.component.scss', changeDetection: ChangeDetectionStrategy.OnPush })
export class PropertyDetailComponent {
  readonly producto = input<Producto | null>(null);
  readonly cerrar = output<void>();
  mostrarEstado(estado: string): string { return estado.replace('_', ' '); }
}
