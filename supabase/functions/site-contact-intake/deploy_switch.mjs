// Non-secret deploy switch for the public contact form.
// false keeps every request at 503 and does not open the database.
// This deployment is explicitly on. Turn it off by setting this to false and redeploying.
// Emergency stop without a code change: CONTACT_INTAKE_ENABLED exactly "false".
export const INTAKE_DEPLOY_ENABLED = true;
