<template>
  <a-layout has-sider>
    <a-layout-sider
      :style="{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
      }"
    >
      <div class="logo">
        <img class="icon" src="/public/logo.png" alt="icon" />
        Momentum
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="workbench">
          <router-link active-class="active" :to="{ name: 'workbench' }">
            <user-outlined />
            <span class="nav-text">工作台</span>
          </router-link>
        </a-menu-item>
        <a-menu-item key="years">
          <router-link active-class="active" :to="{ name: 'years' }">
            <rise-outlined />
            <span class="nav-text">一年新高</span>
          </router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">
      <a-layout-header :style="{ background: '#fff', padding: 0 }" />
      <a-layout-content :style="{ margin: '24px 16px 0', overflow: 'initial' }">
        <RouterView></RouterView>
      </a-layout-content>
      <a-layout-footer :style="{ textAlign: 'center' }">
        Momentum ©2023 Created by Hzx
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script lang="ts">
import {
  UserOutlined,
  RiseOutlined,
} from "@ant-design/icons-vue";
import { defineComponent, ref, computed } from "vue";

import { useRoute } from 'vue-router';

export default defineComponent({
  components: {
    UserOutlined,
    RiseOutlined,
  },
  setup() {
    const route = useRoute();
    
    const selectedKeys = computed({
      get() {
        const [, key] = route.path.split('/');
        return key ? [key] : [];
      },
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      set() {},
    });
    return {
      selectedKeys,
    };
  },
});
</script>

<style scoped>
.logo {
  color: #ffffff;
  font-size: 18px;
  display: flex;
  align-items: center;
  padding: 10px;
}
.logo .icon {
  width: 46px;
  height: 46px;
  margin-right: 10px;
}
.site-layout .site-layout-background {
  background: #fff;
}

[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>
