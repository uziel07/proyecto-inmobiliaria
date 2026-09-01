import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { Producto } from '../../models/producto.model';
@Component({ selector:'app-property-card', standalone:true, imports:[CurrencyPipe], templateUrl:'./property-card.component.html', styleUrl:'./property-card.component.scss', changeDetection:ChangeDetectionStrategy.OnPush })
export class PropertyCardComponent { readonly producto = input.required<Producto>(); readonly seleccionar = output<void>(); }
