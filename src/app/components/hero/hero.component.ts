import { ChangeDetectionStrategy, Component } from '@angular/core';
@Component({ selector:'app-hero', standalone:true, templateUrl:'./hero.component.html', styleUrl:'./hero.component.scss', changeDetection:ChangeDetectionStrategy.OnPush })
export class HeroComponent {}
