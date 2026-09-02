import { CurrencyPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { HeaderComponent } from './components/header/header.component';
import { HeroComponent } from './components/hero/hero.component';
import { MarketInsightsComponent } from './components/market-insights/market-insights.component';
import { NosotrosComponent } from './components/nosotros/nosotros.component';
import { ProductoListComponent } from './components/producto-list/producto-list.component';
import { ClienteListComponent } from './components/cliente-list/cliente-list.component';
import { Producto } from './models/producto.model';

@Component({
  selector: 'app-root',
  imports: [CurrencyPipe, HeaderComponent, HeroComponent, MarketInsightsComponent, NosotrosComponent, ProductoListComponent, ClienteListComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {
  readonly seleccion = signal<Producto[]>([]);
  readonly carritoAbierto = signal(false);

  agregarAlCarrito(producto: Producto): void { this.seleccion.update((items) => items.some((item) => item.id === producto.id) ? items : [...items, producto]); }
  quitarDeSeleccion(id: string): void { this.seleccion.update((items) => items.filter((item) => item.id !== id)); }
  alternarCarrito(): void { this.carritoAbierto.update((abierto) => !abierto); }
}
