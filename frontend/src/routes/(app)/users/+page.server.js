/**
 * Users & Teams Management Page - API Version
 *
 * Migrated from Prisma to Django REST API
 * Allows organization admins to:
 * - View all users in the organization
 * - Add users to the organization by email
 * - Change user roles (ADMIN/USER)
 * - Remove users from the organization
 * - Create, edit, delete teams
 * - Assign users to teams
 *
 * Django Endpoints:
 * - GET    /api/users/                  - List organization users
 * - POST   /api/users/                  - Create new user
 * - GET    /api/user/{id}/              - Get user details
 * - PUT    /api/user/{id}/              - Update user/profile
 * - DELETE /api/user/{id}/              - Deactivate user (soft delete)
 * - GET    /api/teams/                  - List teams
 * - POST   /api/teams/                  - Create team
 * - PUT    /api/teams/{id}/             - Update team
 * - DELETE /api/teams/{id}/             - Delete team
 */
/**
 * Users & Teams Management Page - API Version
 * Migrated from Prisma to Django REST API
 */

import { error, fail } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

// Aseguramos que la URL base termine limpiamente sin barras conflictivas
const API_BASE_URL = `${env.PUBLIC_DJANGO_API_URL}/api`.replace(/\/$/, '');

/**
 * Flatten nested API validation errors into a readable message.
 */
function collectErrorMessages(value) {
  if (!value) return [];
  if (typeof value === 'string') return [value];
  if (Array.isArray(value)) {
    return value.flatMap((item) => collectErrorMessages(item));
  }
  if (typeof value === 'object') {
    return Object.values(value).flatMap((item) => collectErrorMessages(item));
  }
  return [];
}

/**
 * Make authenticated API request
 */
async function apiRequest(endpoint, options = {}, context) {
  const { cookies, org } = context;
  const accessToken = cookies.get('jwt_access');

  // Limpiamos el endpoint para asegurar que comience con '/'
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;

  const response = await fetch(`${API_BASE_URL}${cleanEndpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      'org': org.id,
      ...options.headers
    }
  });

  // Corrección crítica: Validar el estado de respuesta ANTES de asumir que es un JSON parseable
  if (!response.ok) {
    let errorMessage = response.statusText;
    try {
      const errorData = await response.json();
      const messages = collectErrorMessages(errorData.errors || errorData.error || errorData || errorData.detail);
      if (messages.length > 0) errorMessage = messages[0];
    } catch {
      // Si Django explota y devuelve un HTML de error o texto plano
      errorMessage = `Fallo en el servidor backend (Código: ${response.status})`;
    }
    throw new Error(errorMessage);
  }

  return await response.json();
}

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, cookies }) {
  const org = locals.org;
  const user = locals.user;

  try {
    // Normalizamos las rutas de consulta eliminando slashes finales
    const [usersData, teamsData] = await Promise.all([
      apiRequest('/users', {}, { cookies, org }),
      apiRequest('/teams', {}, { cookies, org }).catch(() => ({ teams: [] }))
    ]);

    const activeUsers = usersData.active_users?.active_users || usersData.active_users || [];
    const inactiveUsers = usersData.inactive_users?.inactive_users || usersData.inactive_users || [];

    const currentUserProfile = activeUsers.find(
      (p) => p.user_details?.id === user.id || p.user_details?.email === user.email
    );
    const isAdmin =
      currentUserProfile?.role === 'ADMIN' || currentUserProfile?.is_organization_admin;

    if (!isAdmin) {
      return {
        error: { name: 'No tienes permisos de administrador para acceder a esta sección.' }
      };
    }

    const allUsers = [
      ...activeUsers.map((profile) => ({
        odId: profile.id,
        organizationId: org.id,
        role: profile.role,
        user: {
          id: profile.user_details?.id || profile.id,
          email: profile.user_details?.email || 'N/A',
          name: profile.user_details?.email?.split('@')[0] || 'N/A'
        },
        isActive: true,
        profile
      })),
      ...inactiveUsers.map((profile) => ({
        odId: profile.id,
        organizationId: org.id,
        role: profile.role,
        user: {
          id: profile.user_details?.id || profile.id,
          email: profile.user_details?.email || 'N/A',
          name: profile.user_details?.email?.split('@')[0] || 'N/A'
        },
        isActive: false,
        profile
      }))
    ];

    const teams = (teamsData.teams || teamsData || []).map((team) => ({
      ...team,
      userIds: (team.users || []).map((u) => u.id)
    }));

    return {
      organization: {
        id: org.id,
        name: org.name,
        domain: org.domain || '',
        description: org.description || ''
      },
      users: allUsers,
      teams,
      user: { id: user.id }
    };
  } catch (err) {
    console.error('Error loading users:', err);
    return {
      error: { name: err.message || 'Error al cargar los usuarios del sistema.' }
    };
  }
}

/** @type {import('./$types').Actions} */
export const actions = {
  /**
   * Add user to organization by email
   */
  add_user: async ({ request, locals, cookies }) => {
    const org = locals.org;

    try {
      const formData = await request.formData();
      const email = formData.get('email')?.toString().trim().toLowerCase();
      const role = formData.get('role')?.toString().toUpperCase(); // Forzamos mayúsculas para Django (ADMIN/USER)

      if (!email || !role) {
        return fail(400, { error: 'El correo electrónico y el rol son campos requeridos.' });
      }

      // Estructuramos el payload limpio adaptado a las convenciones del backend
      const userData = { 
        email: email, 
        role: role
      };

      // Apuntamos al endpoint exacto '/users' sin slash final para evitar redirecciones
      await apiRequest(
        '/users',
        {
          method: 'POST',
          body: JSON.stringify(userData)
        },
        { cookies, org }
      );

      return { success: true, action: 'add_user' };
    } catch (err) {
      console.error('Error adding user:', err);
      
      const msg = err.message.toLowerCase();
      if (msg.includes('already exists') || msg.includes('already in organization') || msg.includes('existe')) {
        return fail(400, { error: 'El usuario ya se encuentra registrado en esta organización.' });
      }
      if (msg.includes('not found') || msg.includes('encontrado')) {
        return fail(404, { error: 'No se encontró ningún usuario con ese correo electrónico.' });
      }
      return fail(500, { error: err.message || 'Error interno al procesar la alta de usuario.' });
    }
  },

  /**
   * Edit user role
   */
  edit_role: async ({ request, locals, cookies }) => {
    const org = locals.org;
    const user = locals.user;

    try {
      const formData = await request.formData();
      const user_id = formData.get('user_id')?.toString();
      const role = formData.get('role')?.toString().toUpperCase();

      if (!user_id || !role) {
        return fail(400, { error: 'El ID de usuario y el rol son obligatorios.' });
      }

      if (user_id === user.id) {
        return fail(400, { error: 'No tienes permitido cambiar tu propio rol en el sistema.' });
      }

      await apiRequest(
        `/user/${user_id}`,
        {
          method: 'PATCH',
          body: JSON.stringify({ role })
        },
        { cookies, org }
      );

      return { success: true };
    } catch (err) {
      console.error('Error editing role:', err);
      if (err.message.includes('at least one admin')) {
        return fail(400, { error: 'La organización debe mantener al menos un administrador activo.' });
      }
      return fail(500, { error: err.message || 'Error al actualizar el rol.' });
    }
  },

  /**
   * Remove user from organization (Soft Delete)
   */
  remove_user: async ({ request, locals, cookies }) => {
    const org = locals.org;
    const user = locals.user;

    try {
      const formData = await request.formData();
      const user_id = formData.get('user_id')?.toString();

      if (!user_id) {
        return fail(400, { error: 'El ID de usuario es mandatorio.' });
      }

      if (user_id === user.id) {
        return fail(400, { error: 'No puedes removerte a ti mismo de la organización.' });
      }

      await apiRequest(
        `/user/${user_id}/status`,
        {
          method: 'POST',
          body: JSON.stringify({ status: 'Inactive' })
        },
        { cookies, org }
      );

      return { success: true, action: 'remove_user' };
    } catch (err) {
      console.error('Error removing user:', err);
      if (err.message.includes('at least one admin')) {
        return fail(400, { error: 'La organización debe mantener al menos un administrador activo.' });
      }
      return fail(500, { error: err.message || 'Error al desactivar el usuario.' });
    }
  },

  /**
   * Activate user
   */
  activate_user: async ({ request, locals, cookies }) => {
    const org = locals.org;

    try {
      const formData = await request.formData();
      const user_id = formData.get('user_id')?.toString();

      if (!user_id) {
        return fail(400, { error: 'El ID de usuario es mandatorio.' });
      }

      await apiRequest(
        `/user/${user_id}/status`,
        {
          method: 'POST',
          body: JSON.stringify({ status: 'Active' })
        },
        { cookies, org }
      );

      return { success: true, action: 'activate_user' };
    } catch (err) {
      console.error('Error activating user:', err);
      return fail(500, { error: err.message || 'Error al reactivar el usuario.' });
    }
  },

  /**
   * Create a new team
   */
  create_team: async ({ request, locals, cookies }) => {
    const org = locals.org;

    try {
      const formData = await request.formData();
      const name = formData.get('name')?.toString().trim();
      const description = formData.get('description')?.toString().trim() || '';
      const users = formData.getAll('users').map((u) => u.toString());

      if (!name) {
        return fail(400, { error: 'El nombre del equipo es obligatorio.' });
      }

      await apiRequest(
        '/teams',
        {
          method: 'POST',
          body: JSON.stringify({
            name,
            description,
            assign_users: true,
            users
          })
        },
        { cookies, org }
      );

      return { success: true, action: 'create_team' };
    } catch (err) {
      console.error('Error creating team:', err);
      if (err.message.includes('already exists')) {
        return fail(400, { error: 'Ya existe un equipo registrado con ese nombre.' });
      }
      return fail(500, { error: err.message || 'Error al crear el equipo.' });
    }
  },

  /**
   * Update an existing team
   */
  update_team: async ({ request, locals, cookies }) => {
    const org = locals.org;

    try {
      const formData = await request.formData();
      const teamId = formData.get('team_id')?.toString();
      const name = formData.get('name')?.toString().trim();
      const description = formData.get('description')?.toString().trim() || '';
      const users = formData.getAll('users').map((u) => u.toString());

      if (!teamId || !name) {
        return fail(400, { error: 'El ID de equipo y el nombre son campos obligatorios.' });
      }

      await apiRequest(
        `/teams/${teamId}`,
        {
          method: 'PUT',
          body: JSON.stringify({
            name,
            description,
            assign_users: users
          })
        },
        { cookies, org }
      );

      return { success: true, action: 'update_team' };
    } catch (err) {
      console.error('Error updating team:', err);
      if (err.message.includes('already exists')) {
        return fail(400, { error: 'Ya existe un equipo registrado con ese nombre.' });
      }
      return fail(500, { error: err.message || 'Error al actualizar el equipo.' });
    }
  },

  /**
   * Delete a team
   */
  delete_team: async ({ request, locals, cookies }) => {
    const org = locals.org;

    try {
      const formData = await request.formData();
      const teamId = formData.get('team_id')?.toString();

      if (!teamId) {
        return fail(400, { error: 'El ID de equipo es mandatorio.' });
      }

      await apiRequest(
        `/teams/${teamId}`,
        {
          method: 'DELETE'
        },
        { cookies, org }
      );

      return { success: true, action: 'delete_team' };
    } catch (err) {
      console.error('Error deleting team:', err);
      return fail(500, { error: err.message || 'Error al eliminar el equipo.' });
    }
  }
};
