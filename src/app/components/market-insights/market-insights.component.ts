import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
@Component({ selector:'app-market-insights', standalone:true, templateUrl:'./market-insights.component.html', changeDetection:ChangeDetectionStrategy.OnPush })
export class MarketInsightsComponent { readonly periodo = signal<'Semana'|'Mes'>('Mes'); cambiarPeriodo(value:'Semana'|'Mes'):void { this.periodo.set(value); } }
