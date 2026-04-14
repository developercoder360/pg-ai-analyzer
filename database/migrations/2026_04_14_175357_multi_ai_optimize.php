<?php
/**
 * Multi-AI Consensus Migration: PostgreSQL Integer Optimization
 * Generated: 2026-04-14 17:53:57
 * Models: 2 AI experts consulted
 * Consensus Threshold: 60%
 * 
 * 📊 Analysis:
 * - High Growth Tables: ['attendance_logs', 'attendances']
 * - Warnings: ['Storage savings are secondary to data integrity; all recommendations prioritize safety margins.', 'Rule 1 (current_max × 10 < type_limit) cannot be verified without actual max values; recommend monitoring.', "Verify that 'attendance_id' is not an external API identifier; if it is, revert to bigint per Rule 3.", 'If attendance_logs or attendances experience >200M rows/year, consider table partitioning by date instead of relying solely on bigint.', 'Downgrading bigint to integer requires ALTER TABLE with exclusive locks on large tables; schedule during maintenance windows.', 'Current stats show null max values for attendance tables; assume worst-case growth for safety margin.', 'Ensure all foreign key constraints and application ORM mappings are updated to reflect new integer types to prevent type mismatch errors.']
 */

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        
        try {
            // attendance_logs.user_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: medium | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('attendance_logs', function (Blueprint $table) {
                $table->integer('user_id')->change();
            });
            // attendances.user_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: high | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('user_id')->change();
            });
            // attendances.shift_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('shift_id')->change();
            });
            // attendances.leave_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: medium | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('leave_id')->change();
            });
            // attendances.special_work_day_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('special_work_day_id')->change();
            });
            // attendances.holiday_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: low | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('attendances', function (Blueprint $table) {
                $table->integer('holiday_id')->change();
            });
            // brand_user.user_id: bigint → integer
            // 🤖 Consensus: 100% | Models: qwen/qwen3.6-plus, openrouter/elephant-alpha
            // 📈 Growth: medium | 🔐 Risk: low | 📅 Safe: 5y
            Schema::table('brand_user', function (Blueprint $table) {
                $table->integer('user_id')->change();
            });
            DB::commit();
        } catch (\Exception $e) {
            DB::rollBack();
            throw $e;
        } finally {
            Schema::enableForeignKeyConstraints();
        }
    }

    public function down(): void
    {
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        
        try {
            Schema::table('attendance_logs', function (Blueprint $table) {
                $table->bigInteger('user_id')->change();
            });
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('user_id')->change();
            });
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('shift_id')->change();
            });
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('leave_id')->change();
            });
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('special_work_day_id')->change();
            });
            Schema::table('attendances', function (Blueprint $table) {
                $table->bigInteger('holiday_id')->change();
            });
            Schema::table('brand_user', function (Blueprint $table) {
                $table->bigInteger('user_id')->change();
            });
            DB::commit();
        } catch (\Exception $e) {
            DB::rollBack();
            throw $e;
        } finally {
            Schema::enableForeignKeyConstraints();
        }
    }
};
