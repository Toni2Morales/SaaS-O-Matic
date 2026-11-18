import { Component } from '@angular/core';
import { AppShellComponent } from './core/layout/app-shell';

@Component({
  imports: [AppShellComponent],
  selector: 'app-root',
  templateUrl: './app.html',
})
export class App {}
