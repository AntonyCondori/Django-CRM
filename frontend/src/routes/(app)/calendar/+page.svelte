<script>
  import { onMount } from 'svelte';
  import { Calendar } from '@fullcalendar/core';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import timeGridPlugin from '@fullcalendar/timegrid';
  import PageHeader from '$lib/components/layout/PageHeader.svelte';
  import { SectionCard } from '$lib/components/ui/section-card/index.js';

  let calendarEl;
  let calendar;
  let isLoading = $state(true);


  onMount(() => {
    // Definimos una función asíncrona interna
    async function cargarDatos() {
      try {
        const token = localStorage.getItem('token') || localStorage.getItem('access_token');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;
      // 1. Fetch simultáneo a Google y a tus Tareas locales
      const [resGoogle, resTasks] = await Promise.all([
        fetch('http://localhost:8000/api/auth/google/eventos/', { headers, credentials: 'include' }),
        fetch('http://localhost:8000/api/tasks/', { headers, credentials: 'include' })
      ]);

      const eventosGoogle = resGoogle.ok ? (await resGoogle.json()).eventos : [];
      const listaTareas = resTasks.ok ? await resTasks.json() : [];

      // 2. Mapeo unificado para FullCalendar
      const eventosFinales = [
        ...eventosGoogle.map(e => ({
          title: ` ${e.titulo}`,
          start: e.inicio,
          url: e.enlace,
          backgroundColor: '#4285F4'
        })),
        ...(listaTareas.results || listaTareas).map(t => ({
          title: `✅ ${t.title || t.name}`,
          start: t.due_date,
          backgroundColor: t.priority === 'High' ? '#EF4444' : '#F59E0B'
        }))
      ];

      // 3. Inicializar FullCalendar
      calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin, timeGridPlugin],
        initialView: 'dayGridMonth',
        events: eventosFinales,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek'
        },
        eventClick: (info) => {
          if (info.event.url) {
            info.jsEvent.preventDefault();
            window.open(info.event.url, '_blank');
          }
        }
      });
      calendar.render();
   } catch (err) {
        console.error("Error al cargar eventos:", err);
      } finally {
        isLoading = false;
      }
    }

    // Ejecutamos la función
    cargarDatos();

    // Retornamos la función de limpieza de FullCalendar
    return () => calendar?.destroy();
  });
</script>

<svelte:head>
  <title>Calendar - BottleCRM</title>
</svelte:head>

<PageHeader title="Calenderaio de Eventos y Tareas" subtitle="Google events and CRM tasks" />

<div class="flex-1 p-4 md:p-6">
  <SectionCard class="min-h-[600px] p-4">
    {#if isLoading}
      <div class="flex items-center justify-center h-full">Cargando eventos...</div>
    {/if}
    <div bind:this={calendarEl}></div>
  </SectionCard>
</div>

<style>
  /* Ajuste básico para que el calendario se vea bien en tu layout */
  :global(.fc) { font-family: inherit; }
  :global(.fc-event) { cursor: pointer; padding: 2px; }
</style>