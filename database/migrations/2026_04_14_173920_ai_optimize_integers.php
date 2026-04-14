<?php
/**
 * AI-Generated Migration: PostgreSQL Integer Optimization
 * Generated: 2026-04-14 17:39:20
 * Model: Qwen/Qwen3.6-Plus via OpenRouter
 * 
 * 📊 Analysis Summary:
 * - High Growth Tables: ['attendance_logs', 'attendances']
 * - Warnings: ['Soft-delete pattern (deleted_at) detected across multiple tables. Ensure regular VACUUM and index maintenance to prevent table bloat.', 'attendance_logs and attendances will experience heavy write I/O. Consider partitioning by punch_time or date after 50M+ rows.', 'Downgrading from bigint to integer saves 4 bytes per column per row. For high-volume tables, this significantly reduces index size and improves cache hit ratios.', 'Monitor sequence usage closely. Even with integer, high-throughput systems can exhaust sequences if not configured with CYCLE or proper increment steps.']
 */
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;
return new class extends Migration
{
    /**
     * Run the migrations.
     * OPTIMIZATION: Reduce storage by using smaller integer types
     * SAFETY: All recommendations include 5+ year growth buffer
     */
    public function up(): void
    {
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        try {
            // attendance_logs.attendance_id: bigint → integer
            // 📈 Growth: high | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to attendances table. Max integer limit (2.1B) provides massive safety margin over projected attendance records.
            Schema::table('attendance_logs', function (Blueprint $table) {
                $table->integer('attendance_id')->change();
            });
            // attendance_logs.user_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to users table. User base will not exceed 2.1B in foreseeable future. Integer is optimal for FK joins.
            Schema::table('attendance_logs', function (Blueprint $table) {
                $table->integer('user_id')->change();
            });
            // attendances.user_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to users table. Standard integer capacity is sufficient for any realistic user count.
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('user_id')->change();
            });
            // attendances.shift_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to configuration table. Shift definitions are static/low-growth. Integer provides ample headroom.
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('shift_id')->change();
            });
            // attendances.leave_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to leave types/config. Low cardinality table. Integer is safe and optimizes index size.
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('leave_id')->change();
            });
            // attendances.special_work_day_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to calendar config. Extremely low growth. Integer safely exceeds 10x current max.
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('special_work_day_id')->change();
            });
            // attendances.holiday_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to holiday config. Static reference data. Integer is optimal.
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('holiday_id')->change();
            });
            // authorize_customers.id: bigint → integer
            // 📈 Growth: medium | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Internal primary key. Current max is 443. Integer limit (2.1B) provides >10 year buffer even with aggressive payment growth.
            Schema::table('authorize_customers', function (Blueprint $table) {
                $table->integer('id')->change();
            });
            // authorize_customers.lead_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to leads. Current max 2234. Integer safely accommodates 10x growth margin per rule 5.
            Schema::table('authorize_customers', function (Blueprint $table) {
                $table->integer('lead_id')->change();
            });
            // authorize_nets.id: bigint → integer
            // 📈 Growth: medium | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Internal primary key for transaction logs. Current max 832. Integer provides massive safety buffer for payment volume.
            Schema::table('authorize_nets', function (Blueprint $table) {
                $table->integer('id')->change();
            });
            // brand_user.user_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key mapping table. Current max 664. Integer is standard for relational mappings and saves index space.
            Schema::table('brand_user', function (Blueprint $table) {
                $table->integer('user_id')->change();
            });
            // brand_user.brand_id: bigint → integer
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe for: 10 years
            // 💡 Reason: Foreign key to brands table. Brand count is inherently limited. Integer is optimal for join performance.
            Schema::table('brand_user', function (Blueprint $table) {
                $table->integer('brand_id')->change();
            });
            DB::commit();
            echo "✅ Migrations applied successfully\n";
        } catch (\Exception $e) {
            DB::rollBack();
            echo "❌ Migration failed: " . $e->getMessage() . "\n";
            throw $e;
        } finally {
            Schema::enableForeignKeyConstraints();
        }
    }
    /**
     * Reverse the migrations.
     * Reverts all columns back to BIGINT for safety.
     */
    public function down(): void
    {
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        try {
            // Revert attendance_logs.attendance_id
            Schema::table('attendance_logs', function (Blueprint $table) {
                $table->bigInteger('attendance_id')->change();
            });
            // Revert attendance_logs.user_id
            Schema::table('attendance_logs', function (Blueprint $table) {
                $table->bigInteger('user_id')->change();
            });
            // Revert attendances.user_id
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('user_id')->change();
            });
            // Revert attendances.shift_id
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('shift_id')->change();
            });
            // Revert attendances.leave_id
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('leave_id')->change();
            });
            // Revert attendances.special_work_day_id
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('special_work_day_id')->change();
            });
            // Revert attendances.holiday_id
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('holiday_id')->change();
            });
            // Revert authorize_customers.id
            Schema::table('authorize_customers', function (Blueprint $table) {
                $table->bigInteger('id')->change();
            });
            // Revert authorize_customers.lead_id
            Schema::table('authorize_customers', function (Blueprint $table) {
                $table->bigInteger('lead_id')->change();
            });
            // Revert authorize_nets.id
            Schema::table('authorize_nets', function (Blueprint $table) {
                $table->bigInteger('id')->change();
            });
            // Revert brand_user.user_id
            Schema::table('brand_user', function (Blueprint $table) {
                $table->bigInteger('user_id')->change();
            });
            // Revert brand_user.brand_id
            Schema::table('brand_user', function (Blueprint $table) {
                $table->bigInteger('brand_id')->change();
            });
            DB::commit();
            echo "✅ Rollback completed\n";
        } catch (\Exception $e) {
            DB::rollBack();
            echo "❌ Rollback failed: " . $e->getMessage() . "\n";
            throw $e;
        } finally {
            Schema::enableForeignKeyConstraints();
        }
    }
};
