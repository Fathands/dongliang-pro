<template>
  <div class="years">

    <a-breadcrumb style="margin-bottom: 20px;">
      <a-breadcrumb-item>一年新高</a-breadcrumb-item>
      <a-breadcrumb-item>{{date}}（{{table_list.length}}）</a-breadcrumb-item>
    </a-breadcrumb>

    <a-table
      :columns="columns"
      :data-source="table_list"
      :pagination="false"
      :loading="loading"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'zhangdie'">
          <a-button type="link" :danger="+record.zhangdie >= 0"
            >{{ record.zhangdie }}%</a-button
          >
        </template>
      </template>
    </a-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, getCurrentInstance } from "vue";
import { useRoute } from 'vue-router';

export default defineComponent({
  setup() {
    const instance: any = getCurrentInstance();
    const columns = [
      { title: "股票简称", dataIndex: "name", key: "name" },
      { title: "最新涨跌幅", key: "zhangdie" },
      { title: "所属同花顺行业", dataIndex: "hangye", key: "hangye" },
      { title: "所属概念", dataIndex: "gainian", key: "gainian", width: 400 },
    ];
    const loading = ref(false);
    const table_list = ref([]);
    const route = useRoute();
    const date = route.query.date
    const queryData = () => {
      loading.value = true;
      instance.proxy.$http
        .get("/gateway/api/get_years_data", {
          params: {
            date: date
          },
        })
        .then((res: any) => {
          const list = res.data.data;
          table_list.value = list;
          loading.value = false;
        })
        .catch(() => {
          loading.value = false;
        });
    };

    onMounted(() => {
      queryData();
    });

    return {
      table_list,
      columns,
      loading,
      date
    };
  },
});
</script>

