import { DOCUMENT } from '@angular/common';
import { A11yModule } from '@angular/cdk/a11y';
import { BreakpointObserver } from '@angular/cdk/layout';
import { Component, effect, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter, map, startWith } from 'rxjs';

@Component({
  selector: 'app-shell',
  imports: [
    A11yModule,
    MatButtonModule,
    MatToolbarModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
  ],
  templateUrl: './app-shell.html',
  styleUrl: './app-shell.scss',
})
export class AppShellComponent {
  private readonly router = inject(Router);
  private readonly document = inject(DOCUMENT);
  private readonly breakpointObserver = inject(BreakpointObserver);

  readonly menuOpen = signal(false);
  readonly isMobile = toSignal(
    this.breakpointObserver.observe('(max-width: 767px)').pipe(map((state) => state.matches)),
    { initialValue: false },
  );
  readonly pageTitle = signal('Inicio');

  constructor() {
    effect(() => {
      if (!this.isMobile()) {
        this.menuOpen.set(false);
      }
    });
    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        startWith(null),
      )
      .subscribe(() => this.updatePageContext());
  }

  toggleMenu(): void {
    if (this.menuOpen()) {
      this.dismissMenu();
      return;
    }
    this.menuOpen.set(true);
    queueMicrotask(() => this.document.getElementById('sidebar-close-button')?.focus());
  }

  closeMenu(): void {
    this.menuOpen.set(false);
  }

  dismissMenu(): void {
    this.closeMenu();
    queueMicrotask(() => this.document.getElementById('mobile-menu-toggle')?.focus());
  }

  onMenuKeydown(event: KeyboardEvent): void {
    if (event.key === 'Escape' && this.menuOpen()) {
      this.dismissMenu();
    }
  }

  onNavigation(): void {
    if (this.isMobile()) {
      this.closeMenu();
    }
    queueMicrotask(() => this.document.getElementById('page-title')?.focus());
  }

  private updatePageContext(): void {
    let route = this.router.routerState.snapshot.root;
    while (route.firstChild) {
      route = route.firstChild;
    }
    const title = String(route.data['title'] ?? 'Inicio');
    this.pageTitle.set(title);
    this.document.title = `${title} | SaaS-O-Matic`;
    if (this.isMobile()) {
      this.closeMenu();
      queueMicrotask(() => this.document.getElementById('page-title')?.focus());
    }
  }
}
