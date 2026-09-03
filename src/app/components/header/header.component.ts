import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
@Component({ selector:'app-header', standalone:true, templateUrl:'./header.component.html', changeDetection:ChangeDetectionStrategy.OnPush })
export class HeaderComponent { readonly cantidadCarrito = input(0); readonly abrirCarrito = output<void>(); }
