import { apiRequest } from '$lib/api-helpers.js';

export async function load(event) {
    const { fetch, cookies, url } = event;
    
    // Capturamos el texto de la organización desde la cookie
    const orgIdText = cookies.get('org_id') || '';
    
    // Leemos si viene un límite en la URL o dejamos 50 por defecto
    const limit = url.searchParams.get('limit') || '50';

    let history = [];
    try {
        // CORRECCIÓN DE TIPADO: Convertimos 'org' en el objeto estructurado '{ id: orgIdText }' que exige la firma
        const response = await apiRequest(
            `/auditoria/global/?limit=${limit}`, 
            {}, 
            { cookies, org: { id: orgIdText } }
        );
        
        if (response && !response.error) {
            history = response;
        }
    } catch (e) {
        console.error('Error al conectar con la API de auditoría global:', e);
    }

    return {
        history
    };
}
