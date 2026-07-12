<script>
  import { onMount } from 'svelte';
  import { Calendar, Clock, ExternalLink, AlertCircle } from '@lucide/svelte';
  import PageHeader from '$lib/components/layout/PageHeader.svelte';
  import { SectionCard } from '$lib/components/ui/section-card/index.js';
  import { Button } from '$lib/components/ui/button/index.js';

  let eventos = $state([]);
  let isLoading = $state(true);
  let errorMsg = $state('');

  onMount(async () => {
    try {
      // Intentamos extraer el token (ajusta el nombre si tu CRM usa otra llave como 'access_token')
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      
      // Preparamos las cabeceras
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Si encontramos un token JWT, lo añadimos
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch('http://localhost:8000/api/auth/google/eventos/', {
        method: 'GET',
        headers: headers,
        // CLAVE: Esto envía las cookies de sesión si tu CRM usa el sistema de login de Django
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        eventos = data.eventos;
      } else {
        errorMsg = 'No se pudieron cargar los eventos. Asegúrate de haber conectado tu cuenta de Google Calendar en tu Perfil.';
      }
    } catch (error) {
      errorMsg = 'Error al conectar con el servidor de eventos.';
      console.error(error);
    } finally {
      isLoading = false;
    }
  });

  // Función rápida para dar formato a la fecha/hora de Google
  function formatearFecha(fechaStr) {
    /** @type {Intl.DateTimeFormatOptions} */
    const opciones = { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    };
    return new Date(fechaStr).toLocaleDateString('es-ES', opciones);
  }
</script>

<svelte:head>
  <title>Calendar - BottleCRM</title>
</svelte:head>

<PageHeader title="Calendar" subtitle="Your upcoming events and meetings" />

<div class="flex-1 space-y-6 p-4 md:p-6">
  {#if isLoading}
    <div class="flex items-center justify-center p-12">
      <div class="h-8 w-8 animate-spin rounded-full border-4 border-[var(--color-primary-default)] border-t-transparent"></div>
    </div>
  {:else if errorMsg}
    <SectionCard padded={false} class="border-[var(--color-negative-default)]/20 bg-[var(--color-negative-light)] p-6">
      <div class="flex flex-col items-center justify-center text-center gap-3">
        <AlertCircle class="h-10 w-10 text-[var(--color-negative-default)]" />
        <p class="text-foreground font-medium">{errorMsg}</p>
        <Button variant="outline" class="mt-2" onclick={() => window.location.href = '/profile'}>
          Go to Profile Settings
        </Button>
      </div>
    </SectionCard>
  {:else if eventos.length === 0}
    <SectionCard>
      <div class="flex flex-col items-center justify-center py-12 text-center text-muted-foreground">
        <Calendar class="h-12 w-12 mb-4 opacity-50" />
        <p>No tienes eventos próximos en tu calendario.</p>
      </div>
    </SectionCard>
  {:else}
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {#each eventos as evento}
        <SectionCard padded={true} class="flex flex-col justify-between hover:shadow-md transition-shadow h-full">
          <div>
            <h3 class="text-foreground font-semibold text-lg line-clamp-2 mb-2">
              {evento.titulo}
            </h3>
            <div class="flex items-center gap-2 text-sm text-muted-foreground mb-4">
              <Clock class="h-4 w-4 shrink-0" />
              <span>{formatearFecha(evento.inicio)}</span>
            </div>
          </div>
          
          {#if evento.enlace}
            <a 
              href={evento.enlace} 
              target="_blank" 
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-sm font-medium text-[var(--color-primary-default)] hover:underline mt-auto pt-4"
            >
              <ExternalLink class="h-4 w-4" />
              Ver en Google Calendar
            </a>
          {/if}
        </SectionCard>
      {/each}
    </div>
  {/if}
</div>