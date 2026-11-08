// Public form switch. The server still rejects invalid input and stays closed
// when deploy_switch.mjs is not exactly true, or CONTACT_INTAKE_ENABLED is "false".
// enabled must be exactly true and endpoint must be an https URL or the button stays disabled.
window.SEISHINKAI_CONTACT_INTAKE = {
  enabled: true,
  endpoint: "https://zvrardoyxocmqhvyddnf.supabase.co/functions/v1/site-contact-intake"
};
