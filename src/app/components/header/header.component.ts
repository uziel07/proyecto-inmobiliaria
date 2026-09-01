import { ChangeDetectionStrategy, Component, input } from '@angular/core';
@Component({ selector:'app-header', standalone:true, templateUrl:'./header.component.html', styleUrl:'./header.component.scss', changeDetection:ChangeDetectionStrategy.OnPush })
export class HeaderComponent { readonly cantidadCarrito = input(0); }
