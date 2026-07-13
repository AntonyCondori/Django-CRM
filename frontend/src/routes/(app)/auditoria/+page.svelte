<script>
    import PageHeader from '$lib/components/layout/PageHeader.svelte';
    import SectionCard from '$lib/components/ui/section-card/index.js'; // O la ruta de SectionCard de tus leads

    // Recibimos los datos inyectados desde el servidor (+page.server.js)
    let { data } = $props();
    const fullHistory = $derived(data.history || []);

    // Estado reactivo para controlar el filtro seleccionado por el usuario
    let selectedModule = $state('Todos');

    // Filtramos la lista en tiempo real según el botón o selector activo
    const filteredHistory = $derived(
        selectedModule === 'Todos'
            ? fullHistory
            : fullHistory.filter(item => item.module === selectedModule)
    );
</script>

<PageHeader title="Panel General de Auditoría del CRM" />

<div class="p-6 space-y-6">
    <!-- BARRA DE FILTROS POR MÓDULO -->
    <div class="flex items-center gap-2 bg-[color:var(--bg-elevated)] p-3 rounded-lg border border-[color:var(--border-faint)]">
        <span class="text-[12px] font-medium text-[color:var(--text-subtle)] mr-2">Filtrar por Módulo:</span>
        {#each ['Todos', 'Lead', 'Contacto', 'Cuenta', 'Oportunidad'] as mod}
            <button
                onclick={() => selectedModule = mod}
                class="px-3 py-1 text-[12px] font-medium rounded-md transition-colors
                    {selectedModule === mod 
                        ? 'bg-blue-600 text-white shadow-sm' 
                        : 'bg-transparent text-[color:var(--text-muted)] hover:bg-[color:var(--sidebar-accent)]'}"
            >
                {mod === 'Todos' ? 'Todos los Módulos' : mod}
            </button>
        {/each}
    </div>

    <!-- CONTENEDOR PRINCIPAL DE LA TABLA -->
    <SectionCard title="Registro de Operaciones Globales">
        {#if filteredHistory.length === 0}
            <p class="text-[12px] italic text-[color:var(--text-subtle)] py-4">No se encontraron movimientos registrados para el filtro seleccionado.</p>
        {:else}
            <div class="overflow-x-auto">
                <table class="w-full text-left text-[12px] border-collapse">
                    <thead>
                        <tr class="bg-[color:var(--bg-elevated)] text-[color:var(--text-subtle)] font-medium border-b border-[color:var(--border-faint)]">
                            <th class="p-3">Fecha y Hora</th>
                            <th class="p-3">Módulo afectado</th>
                            <th class="p-3">Registro original</th>
                            <th class="p-3">Usuario responsable</th>
                            <th class="p-3">Operación</th>
                            <th class="p-3">Detalle de Cambios</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-[color:var(--border-faint)]">
                        {#each filteredHistory as log}
                            <tr class="hover:bg-[color:var(--bg-elevated)]/30">
                                <td class="p-3 text-[color:var(--text-muted)] whitespace-nowrap">
                                    {new Date(log.history_date).toLocaleString()}
                                </td>
                                <td class="p-3">
                                    <span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-gray-100 text-gray-700">
                                        {log.module}
                                    </span>
                                </td>
                                <td class="p-3 font-medium text-[color:var(--text)] truncate max-w-[150px]" title={log.object_name}>
                                    {log.object_name}
                                </td>
                                <td class="p-3 font-medium text-blue-600 truncate max-w-[180px]" title={log.history_user}>
                                    {log.history_user}
                                </td>
                                <td class="p-3">
                                    <span class="px-2 py-0.5 rounded text-[11px] font-semibold 
                                        {log.history_type === 'Creación' ? 'bg-green-100 text-green-700' : ''}
                                        {log.history_type === 'Modificación' ? 'bg-amber-100 text-amber-700' : ''}
                                        {log.history_type === 'Eliminación' ? 'bg-red-100 text-red-700' : ''}">
                                        {log.history_type}
                                    </span>
                                </td>
                                <td class="p-3 text-[color:var(--text)]">
                                    {#each log.changes as change}
                                        <div class="my-0.5">
                                            <strong class="text-[color:var(--text-muted)]">{change.field}:</strong> 
                                            {#if change.old}
                                                <span class="line-through text-red-500 bg-red-50 px-1 rounded">{change.old}</span>
                                            {:else}
                                                <span class="italic text-gray-400">vacío</span>
                                            {/if}
                                            <span class="mx-1">→</span>
                                            <span class="text-green-700 bg-green-50 px-1 rounded font-medium">{change.new}</span>
                                        </div>
                                    {/each}
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}
    </SectionCard>
</div>
