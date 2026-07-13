<script>
  import { onMount, tick } from 'svelte';
  import { Calendar } from '@fullcalendar/core';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import timeGridPlugin from '@fullcalendar/timegrid';
  import PageHeader from '$lib/components/layout/PageHeader.svelte';
  import { SectionCard } from '$lib/components/ui/section-card/index.js';

  let calendarEl;
  let calendar;
  let isLoading = $state(true);

  // --- Variables de Estado para el Formulario ---
  let titulo = $state('');
  let fechaInicio = $state('');
  let fechaFin = $state('');
  let isSubmitting = $state(false);

  // --- Extraemos cargarDatos para poder reutilizarla ---
  async function cargarDatos() {
    isLoading = true;
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const orgId = localStorage.getItem('org') || localStorage.getItem('tenant_id') || '';

      const headers = { 
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
        'org': orgId 
      };

      const [resGoogle] = await Promise.all([
        fetch('http://localhost:8000/api/auth/google/eventos/', { headers, credentials: 'include' }),
  
      ]);

      const dataGoogle = resGoogle.ok ? await resGoogle.json() : {};

      const eventosFinales = [
          ...(dataGoogle.eventos || []).map(e => {
          const fechaInicio = new Date(e.inicio).toISOString();

          return {
            title: e.titulo || 'Reunión sin título',
            start: fechaInicio, // FullCalendar requiere estrictamente la propiedad 'start'
            url: e.enlace,
            backgroundColor: '#4285F4',
            borderColor: '#4285F4',
            textColor: '#ffffff'
          };
        })
      ];

      isLoading = false;
      await tick(); 

      if (calendarEl) {
        // Destruimos el calendario previo si estamos actualizando los datos
        if (calendar) calendar.destroy();

        calendar = new Calendar(calendarEl, {
          plugins: [dayGridPlugin, timeGridPlugin],
          initialView: 'dayGridMonth',
          events: eventosFinales,
          timeZone: 'local', // Esto fuerza a FullCalendar a ajustar los eventos a la hora del navegador
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
      }
    } catch (err) {
      console.error("Error crítico al cargar calendario:", err);
      isLoading = false; 
    }
  }

  // --- Función para enviar el evento a Django ---
async function guardarEventoGoogle() {
  if (!titulo || !fechaInicio || !fechaFin) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  isSubmitting = true;
  try {
    // Obtenemos el CSRF token de las cookies para que Django no bloquee el POST
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    };

    const response = await fetch('http://localhost:8000/api/auth/google/eventos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // <--- ESTO ES LO QUE TE FALTABA
        'org': getCookie('org') // Django busca la org aquí también
      },
      credentials: 'include', // <--- Esto envía automáticamente el jwt_access y sessionid
      body: JSON.stringify({
        summary: titulo,
        start_time: new Date(fechaInicio).toISOString(),
        end_time: new Date(fechaFin).toISOString()
      })
    });

    if (response.ok) {
      alert("¡Evento creado con éxito!");
      titulo = '';
      fechaInicio = '';
      fechaFin = '';
      cargarDatos();
    } else {
      const err = await response.json();
      console.error("Error del backend:", err);
      alert("Error: " + (err.error || "No autorizado"));
    }
  } catch (error) {
    console.error("Error:", error);
  } finally {
    isSubmitting = false;
  }
}

  onMount(() => {
    cargarDatos();
    return () => calendar?.destroy();
  });
</script>

<svelte:head>
  <title>Calendar - BottleCRM</title>
</svelte:head>

<PageHeader title="Calendario de Eventos y Tareas" subtitle="Google events and CRM tasks" />

<div class="flex-1 p-4 md:p-6">
  <!-- Layout de cuadrícula: 1 columna para el form, 3 para el calendario -->
  <div class="grid grid-cols-1 xl:grid-cols-4 gap-6">
    
    <!-- COLUMNA IZQUIERDA: Formulario -->
    <div class="xl:col-span-1">
      <SectionCard class="p-4 bg-white h-max">
        <h3 class="text-lg font-bold mb-4 pb-2 border-b">Nuevo Evento de Google</h3>
        
        <form on:submit|preventDefault={guardarEventoGoogle} class="flex flex-col gap-4">
          <label class="flex flex-col text-sm font-medium">
            Título del evento
            <input 
              type="text" 
              bind:value={titulo} 
              required 
              placeholder="Ej: Reunión con cliente"
              class="border p-2 rounded mt-1 font-normal focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </label>

          <label class="flex flex-col text-sm font-medium">
            Fecha de Inicio
            <input 
              type="datetime-local" 
              bind:value={fechaInicio} 
              required 
              class="border p-2 rounded mt-1 font-normal focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </label>

          <label class="flex flex-col text-sm font-medium">
            Fecha de Fin
            <input 
              type="datetime-local" 
              bind:value={fechaFin} 
              required 
              class="border p-2 rounded mt-1 font-normal focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </label>

          <button 
            type="submit" 
            disabled={isSubmitting} 
            class="bg-blue-600 text-white font-medium p-2 rounded hover:bg-blue-700 transition-colors disabled:bg-blue-400 mt-2"
          >
            {isSubmitting ? 'Guardando...' : 'Crear un Evento'}
          </button>
        </form>
      </SectionCard>
    </div>

    <!-- COLUMNA DERECHA: Calendario -->
    <div class="xl:col-span-3">
      <SectionCard class="min-h-[600px] p-4">
        {#if isLoading}
          <div class="flex items-center justify-center h-full min-h-[500px]">
            <p class="text-gray-500 font-medium">Cargando eventos y tareas...</p>
          </div>
        {:else}
          <div bind:this={calendarEl}></div>
        {/if}
      </SectionCard>
    </div>

  </div>
</div>

<style>
  :global(.fc) { font-family: inherit; }
  :global(.fc-event) { cursor: pointer; padding: 2px; border: none; }
</style>