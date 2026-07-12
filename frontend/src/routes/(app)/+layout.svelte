<script>
  import '../../app.css';
  import { AppShell } from '$lib/components/layout/index.js';
  import { Toaster } from '$lib/components/ui/sonner/index.js';
  import { initOrgSettings } from '$lib/stores/org.js';

  let { data, children } = $props();

  // Initialize org settings store from server data
  $effect(() => {
    if (data.org_settings) {
      initOrgSettings(data.org_settings);
    }
  });
</script>

<svelte:head>
  <script type="module">
    import Chatbot from "https://cdn.jsdelivr.net/npm/flowise-embed/dist/web.js"
    Chatbot.init({
      chatflowid: "fee610c9-7f9c-4aad-ad63-269fac3b2d48",
      apiHost: "https://cloud.flowiseai.com",
      chatflowConfig: {
        vars: { assistantToken: data.assistantToken }
      }
    })
  </script>
</svelte:head>

<AppShell user={data.user} org_name={data.org_name} org_settings={data.org_settings}>
  <main class="relative flex-1">
    {@render children()}
  </main>
</AppShell>

<Toaster richColors closeButton position="bottom-right" />
