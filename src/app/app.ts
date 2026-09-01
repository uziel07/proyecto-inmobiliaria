import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { HeaderComponent } from './components/header/header.component';
import { HeroComponent } from './components/hero/hero.component';
import { MarketInsightsComponent } from './components/market-insights/market-insights.component';
import { ProductoListComponent } from './components/producto-list/producto-list.component';

@Component({
  selector: 'app-root',
  imports: [HeaderComponent, HeroComponent, MarketInsightsComponent, ProductoListComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {
  readonly carrito = signal(0);

  agregarAlCarrito(): void { this.carrito.update((value) => value + 1); }
}
