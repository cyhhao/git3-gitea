import { createApp } from 'vue';
import Git3RepoCreate from '../components/Git3RepoCreate.vue';

export function initGit3Mount() {
  const el = document.getElementById('git3-repo-create');
  if (!el) return;

  const view = createApp(Git3RepoCreate);
  view.mount(el);
  console.log("mounted git3");

}
